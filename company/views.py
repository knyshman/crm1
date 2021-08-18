import stats as stats
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from .forms import *
from .models import Company, Project
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class CompanyListView(LoginRequiredMixin, ListView):
    """Generic class-based view for a list of companies for authenticated users"""
    model = Company
    paginate_by = 10
    template_name = 'company/company_list.html'
    ordering = 'name'

    def get_ordering(self):
        """Get ordering for companies in companies' list"""
        ordering = self.request.GET.get('sort', 'name')
        return ordering if ordering in {'name', '-name', 'date_create', '-date_create'} else 'name'

    def get_context_data(self, *, object_list=None, **kwargs):
        """Add current order to context data"""
        context = super(CompanyListView, self).get_context_data(**kwargs)
        context['current_order'] = self.get_ordering()
        return context


class CompanyDetailView(LoginRequiredMixin, DetailView):
    """Generic class-based detail view for a company for authenticated users"""
    model = Company
    template_name = 'company/company_detail.html'


class CompanyCreateView(PermissionRequiredMixin, CreateView):
    """Create new company only if user can add company"""
    model = Company
    form_class = CompanyForm
    template_name = 'company/company_create.html'
    permission_required = 'company.add_company'

    def get_context_data(self, **kwargs):
        """Add formsets' data to company's context"""
        context = super(CompanyCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['phone_formset'] = PhoneFormset(self.request.POST, instance=self.object)
            context['email_formset'] = EmailFormSet(self.request.POST, instance=self.object)
            context['manager_formset'] = ManagerFormSet(self.request.POST, instance=self.object)
            context['phone_formset'].full_clean()
            context['email_formset'].full_clean()
            context['manager_formset'].full_clean()
        else:
            context['phone_formset'] = PhoneFormset(instance=self.object)
            context['email_formset'] = EmailFormSet(instance=self.object)
            context['manager_formset'] = ManagerFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        """Check if form valid"""
        context = self.get_context_data(form=form)
        phone_formset = context['phone_formset']
        email_formset = context['email_formset']
        manager_formset = context['manager_formset']
        if phone_formset.is_valid() and email_formset.is_valid() and manager_formset.is_valid():
            response = super().form_valid(form)
            phone_formset.instance = self.object
            phone_formset.save()
            email_formset.instance = self.object
            email_formset.save()
            manager_formset.instance = self.object
            manager_formset.save()
            return response
        else:
            return super().form_invalid(form)


class CompanyUpdateView(PermissionRequiredMixin, UpdateView):
    """Update current company view if user can change data of company"""
    model = Company
    fields = '__all__'
    template_name = 'company/company_update.html'
    permission_required = 'company.change_company'

    def get_context_data(self, **kwargs):
        """Add formsets' data to company's context"""
        context = super(CompanyUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['phone_formset'] = PhoneFormset(self.request.POST, instance=self.object)
            context['email_formset'] = EmailFormSet(self.request.POST, instance=self.object)
            context['manager_formset'] = ManagerFormSet(self.request.POST, instance=self.object)
            context['phone_formset'].full_clean()
            context['email_formset'].full_clean()
            context['manager_formset'].full_clean()
        else:
            context['phone_formset'] = PhoneFormset(instance=self.object)
            context['email_formset'] = EmailFormSet(instance=self.object)
            context['manager_formset'] = ManagerFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        """Check if form and formsets are valid"""
        context = self.get_context_data(form=form)
        phone_formset = context['phone_formset']
        email_formset = context['email_formset']
        manager_formset = context['manager_formset']
        if phone_formset.is_valid() and email_formset.is_valid() and manager_formset.is_valid():
            response = super().form_valid(form)
            phone_formset.instance = self.object
            phone_formset.save()
            email_formset.instance = self.object
            email_formset.save()
            manager_formset.instance = self.object
            manager_formset.save()
            return response
        else:
            return super().form_invalid(form)


class CompanyDeleteView(PermissionRequiredMixin, DeleteView):
    """Delete current company if user can change company"""
    model = Company
    success_url = reverse_lazy('company_list')
    template_name = 'company/company_delete.html'
    permission_required = 'company.change_company'


class ProjectListView(LoginRequiredMixin, ListView):
    """Generic class-based view for a list of projects for authenticated users"""
    model = Project
    paginate_by = 10
    template_name = 'company/project_list.html'


class ProjectDetailView(LoginRequiredMixin, DetailView):
    """Detail view of a project for authenticated users"""
    model = Project
    template_name = 'company/project_detail.html'


class ProjectCreateView(PermissionRequiredMixin, CreateView):
    """Create a new project if user can add project"""
    model = Project
    fields = '__all__'
    template_name = 'company/project_create.html'
    permission_required = 'company.add_project'


class ProjectUpdateView(PermissionRequiredMixin, UpdateView):
    """Update current project if user can change project"""
    model = Project
    fields = '__all__'
    template_name = 'company/project_create.html'
    permission_required = 'company.change_project'


class ProjectDeleteView(PermissionRequiredMixin, DeleteView):
    """Delete current project if user can delete project"""
    model = Project
    template_name = 'company/project_delete.html'
    permission_required = 'company.delete_project'

    def get_success_url(self):
        return reverse_lazy('company_detail', kwargs={'pk': self.object.company_id})


class InteractionByCompanyList(PermissionRequiredMixin, ListView):
    """Representing a list of interactions for current company"""
    model = Company
    permission_required = 'management.view_interaction'
    template_name = 'company/interaction_by_company_list.html'
    paginate_by = 10

    def get_queryset(self):
        """Get queryset for current company"""
        qs = Company.objects.prefetch_related('interactions').filter(pk=self.kwargs['pk'])
        obj_list = []
        for obj in qs:
            grade = str(round(stats.mean([interaction.grade for interaction in obj.interactions.all()]), 2))
            channel = [interaction.channel for interaction in obj.interactions.all()]
            pk = [interaction.pk for interaction in obj.interactions.all()]
            project = [interaction.project for interaction in obj.interactions.all()]
            for i in range(len(obj.interactions.all())):
                obj_list.append({'id': obj.id, 'name': obj.name, 'grade': grade, 'project': project[i], 'channel': channel[i], 'pk': str(pk[i])})
        return obj_list


class InteractionByProjectList(PermissionRequiredMixin, ListView):
    """Representing a list of interactions for current project"""
    model = Project
    permission_required = 'management.view_interaction'
    template_name = 'company/interactions_by_project.html'
    paginate_by = 10

    def get_queryset(self):
        """Get queryset for current project"""
        qs = Project.objects.prefetch_related('interactions').filter(pk=self.kwargs['pk'])
        obj_list = []
        for obj in qs:
            channel = [interaction.channel for interaction in obj.interactions.all()]
            pk = [interaction.pk for interaction in obj.interactions.all()]
            for i in range(len(obj.interactions.all())):
                obj_list.append({'id': obj.id, 'name': obj.project, 'company': obj.company.name, 'channel': channel[i], 'pk': str(pk[i])})
        return obj_list

