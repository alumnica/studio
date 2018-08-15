from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import FormView

from alumnica_model.models import Ambit, users, Subject, ODA


class ApproveToPublishDashboard(LoginRequiredMixin, FormView):
    login_url = "login_view"
    template_name = "studio/dashboard/supervisor.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.user_type != users.TYPE_SUPERVISOR:
            return redirect(to="dashboard_view")
        else:
            return super(ApproveToPublishDashboard, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        ambits = Ambit.objects.filter(is_draft=False, is_published=False)
        ambits_list = []
        for ambit in ambits:
            odas = [len(subject.odas.all()) for subject in ambit.subjects.all()]
            moments = []
            for subject in ambit.subjects.all():
                for oda in subject.odas.all():
                    moments = [len(microoda.activities.all()) for microoda in oda.microodas.all()]

            ambits_list.append([ambit, sum(odas), sum(moments)])
        return {'ambits_list': ambits_list}


class AmbitPreviewView(LoginRequiredMixin, FormView):
    login_url = "login_view"
    template_name = "studio/dashboard/supervisor-vp-ambito.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.user_type != users.TYPE_SUPERVISOR:
            return redirect(to="dashboard_view")
        else:
            return super(AmbitPreviewView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {}
        ambit = Ambit.objects.get(pk=self.kwargs['pk'])
        context.update({'ambit': ambit})
        return context


class GridPositionView(LoginRequiredMixin, FormView):
    login_url = "login_view"
    template_name = "studio/dashboard/supervisor-drag-drop.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.user_type != users.TYPE_SUPERVISOR:
            return redirect(to="dashboard_view")
        else:
            return super(GridPositionView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {}
        ambits_list = Ambit.objects.filter(is_published=True).order_by('position')
        pk = self.kwargs['pk']
        if pk > 0:
            ambit = Ambit.objects.get(pk=self.kwargs['pk'])
            context.update({'new_ambit': ambit})
        context.update({'ambits_list': ambits_list})
        return context

    def post(self, request, *args, **kwargs):
        position_array = self.request.POST.get('order').split(',')
        counter = 1
        for element in position_array:
            ambit = Ambit.objects.get(pk=int(element))
            ambit.position = counter
            ambit.is_draft = False
            ambit.is_published = True
            ambit.save()
            counter += 1
        return redirect(to="dashboard_view")


class ODAsPositionSubjectPreview(LoginRequiredMixin, FormView):
    login_url = "login_view"
    template_name = "studio/dashboard/supervisor-vp-materia.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.user_type != users.TYPE_SUPERVISOR:
            return redirect(to="dashboard_view")
        else:
            return super(ODAsPositionSubjectPreview, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {}
        subject = Subject.objects.get(pk=self.kwargs['pk'])
        section_images_list = subject.sections_images.all()
        odas_list = []
        section_counter = 1
        for section in subject.sections_images.all():
            odas_list.append(subject.odas.all().filter(section=section_counter))
            section_counter += 1

        zones = ['a', 'b', 'c', 'd']
        subject_zip = zip(section_images_list, zones)
        context.update({'subject_zip': subject_zip, 'odas_list': odas_list, 'ambit_pk': subject.ambit.pk})
        return context


class MicroodaPreview(LoginRequiredMixin, FormView):
    login_url = "login_view"
    template_name = "studio/dashboard/supervisor-vp-oda.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.user_type != users.TYPE_SUPERVISOR:
            return redirect(to="dashboard_view")
        else:
            return super(MicroodaPreview, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {}
        oda = ODA.objects.get(pk=self.kwargs['pk'])
        context.update({'oda': oda})
        return context
