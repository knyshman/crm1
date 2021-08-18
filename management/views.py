from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from . import models, forms


class KeywordsChannel:
    """Get all keywords and all channels for the filter of interactions"""
    def get_keywords(self):
        keywords = models.Keyword.objects.values('keyword')
        return keywords

    def get_channel(self):
        """Get all channels in interactions' objects"""
        return models.Interaction.objects.values('channel').distinct()


class KeywordCreate(PermissionRequiredMixin, CreateView):
    """Create a new keyword for interactions' filter"""
    model = models.Keyword
    fields = '__all__'
    permission_required = 'management.view_interaction'


class InteractionList(PermissionRequiredMixin, ListView, KeywordsChannel):
    """Generic class-based view for a list of interactions if user can view interactions"""
    model = models.Interaction
    permission_required = 'management.view_interaction'
    ordering = '-grade'
    template_name = 'management/all_interactions.html'
    paginate_by = 10

    def get_queryset(self):
        """Return interactions in according with keywords"""
        qs = super(InteractionList, self).get_queryset()
        q_lst = self.request.GET.getlist("q")
        if q_lst:
            q = '|'.join(q_lst)
            return qs.filter(Q(channel__iregex=q) | Q(description__iregex=q)).distinct()
        return qs


class InteractionDetail(PermissionRequiredMixin, DetailView):
    """Generic class-based view for an interaction if user can view interactions"""
    model = models.Interaction
    template_name = 'management/interaction_detail.html'
    permission_required = 'management.view_interaction'


class InteractionCreate(PermissionRequiredMixin, CreateView):
    """Create a new interaction if user can add interactions"""
    model = models.Interaction
    fields = '__all__'
    permission_required = 'management.add_interaction'


class InteractionUpdate(PermissionRequiredMixin, UpdateView):
    """Update current interaction if user can change interactions"""
    model = models.Interaction
    fields = '__all__'
    permission_required = 'management.change_interaction'

    def has_permission(self):
        """Check if current user has permission"""
        perms = self.get_permission_required()
        if self.request.user.username != self.get_object().manager.username:
            raise ValidationError()
        return self.request.user.has_perms(perms)


class InteractionDelete(PermissionRequiredMixin, DeleteView):
    """Delete current interaction if user can delete interactions"""
    model = models.Interaction
    template_name = 'management/interaction_delete.html'
    success_url = reverse_lazy('interaction_list')
    permission_required = 'management.delete_interaction'

    def has_permission(self):
        """Check if current user has permission"""
        perms = self.get_permission_required()
        if self.request.user.username != self.get_object().manager.username:
            raise ValidationError()
        return self.request.user.has_perms(perms)


class ManagerDetail(PermissionRequiredMixin, DetailView):
    """Representing user's profile if user can view users"""
    model = models.User
    template_name = 'management/manager_detail.html'
    permission_required = 'management.view_user'

    def get_object(self, queryset=None):
        return self.request.user


class ManagerUpdate(PermissionRequiredMixin, UpdateView):
    """Update self manager's profile if manager is current user"""
    form_class = forms.UserForm
    template_name = 'management/manager_update.html'
    permission_required = 'management.view_interaction'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        if form.is_valid:
            obj = form.save(commit=False)
            if obj.password.startswith('pbkdf2_sha256'):
                obj.save()
            else:
                obj.password = make_password(obj.password)
                obj.save()
            return super().form_valid(form)

    def get_success_url(self):
        """Get success url after updating"""
        return reverse('manager_detail')


class InteractionListByManager(PermissionRequiredMixin, ListView, KeywordsChannel):
    """Representing an interaction list of current user"""
    model = models.Interaction
    template_name = 'management/interaction_by_manager_list.html'
    permission_required = 'management.view_interaction'
    paginate_by = 10

    def get_queryset(self):
        """Return current user's interactions in accordance with keywords"""
        manager = self.request.user
        qs = super(InteractionListByManager, self).get_queryset().filter(manager=manager)
        q_lst = self.request.GET.getlist("q")
        if q_lst:
            q = '|'.join(q_lst)
            return qs.filter(Q(channel__iexact=q) | Q(description__iregex=q)).distinct()
        return qs

