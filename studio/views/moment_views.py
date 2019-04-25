from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DetailView

from alumnica_model.mixins import OnlyContentCreatorAndSupervisorMixin
from alumnica_model.models import Moment, Tag
from alumnica_model.models.content import typeMoment, Subject
from studio.forms.moment_forms import MomentCreateForm, MomentUpdateForm
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt


class MomentsView(LoginRequiredMixin, OnlyContentCreatorAndSupervisorMixin, ListView):
    """
    Momentos dashboard view
    """
    login_url = 'login_view'
    template_name = 'studio/dashboard/momentos.html'
    queryset = Moment.objects.all()
    context_object_name = 'moments_list'


class CreateMomentView(LoginRequiredMixin, CreateView):
    """
    Create new Momento object view
    """
    login_url = 'login_view'
    template_name = 'studio/dashboard/momentos-edit.html'
    form_class = MomentCreateForm

    # def _save_content(self):
    #     content = self['content']
    #     print ('in _save_content')
    #     print (content)

    #     #s3 = S3Boto3Storage()

    #     s3_filename = os.path.join('temp', str(uuid.uuid4()))
    #     with s3.open(s3_filename, 'wb') as s3_file:
    #         _logger.debug('Uploading {} to {}'.format(content.name, s3_filename))
    #         for chunk in content.chunks(chunk_size=s3_file.buffer_size):
    #             wrote = s3_file.write(chunk)
    #             _logger.debug('Transmitted {} bytes to S3'.format(filesizeformat(wrote)))

        #q = Queue(connection=worker.conn)
    #  return #q.enqueue(save_h5package, s3_filename, timeout=600)


    def get_context_data(self, **kwargs):
        print ('create momentos')
        print (self)
        print (kwargs)
        print (kwargs.get('name'))
        print (kwargs.get('h5p-name'))
        
             
        moments_list = Moment.objects.all()
        tags = Tag.objects.all()
        moment_type_list = typeMoment.values() #MomentType.objects.all()
        print (moment_type_list)
        subjects_list = []
        odas_list = []

        for subject in Subject.objects.all():
            odas = []
            microodas_list = []

            if subject.ambit is not None:
                if not subject.ambit.is_draft:
                    continue

            for oda in subject.odas.all():
                microodas = []
                for microoda in oda.microodas.all():
                    if microoda.activities.all().count() < 3:
                        microodas.append(microoda.type.name)

                if len(microodas) > 0:
                    odas.append(oda)
                    microodas_list.append(microodas)
            if len(odas) > 0:
                odas_zip = zip(odas, microodas_list)
                odas_list.append(odas_zip)
                subjects_list.append(subject)        
        subject_odas = zip(subjects_list, odas_list)
        #print (subject_odas)

        context = super(CreateMomentView, self).get_context_data(**kwargs)
        print (context)
        context.update({'moments_list': moments_list,
                        'tags': tags,
                        'subject_odas': subject_odas,
                        'moment_type_list': moment_type_list})
        print ('out get_context_data')
        return context

    def form_valid(self, form):
        print (' valud save data after upload files ')
        subject = self.request.POST.get('materia-list')
        oda = self.request.POST.get('oda-list')
        microoda = self.request.POST.get('micro-oda')
        moment_type = self.request.POST.get('tipo-momento')
        print (moment_type)
        #if moment_type == typeMoment.mp3 or moment_type == typeMoment.img:
         #   self._save_content()
        #h5p_job_id = self.request.POST.get('url_h5p')
        form.save_form(self.request.user, subject, oda, microoda, moment_type) # h5p_job_id)
        return redirect(to='momentos_view')


class UpdateMomentView(LoginRequiredMixin, OnlyContentCreatorAndSupervisorMixin, UpdateView):
    """
    Update existing Momento view
    """
    login_url = 'login_view'
    template_name = 'studio/dashboard/momentos-edit.html'
    form_class = MomentUpdateForm

    def get_object(self, queryset=None):
        return Moment.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        print ('update momentos')
        moments_list = Moment.objects.all()
        tags = Tag.objects.all()
        moment_type_list = typeMoment.values #MomentType.objects.all()
        subjects_list = []
        odas_list = []

        for subject in Subject.objects.all():
            odas = []
            microodas_list = []

            if subject.ambit is not None:
                if self.object.microoda is not None:
                    if not subject.ambit.is_draft and self.object.microoda.oda.subject != subject:
                        continue

            for oda in subject.odas.all():
                microodas = []
                for microoda in oda.microodas.all():
                    if microoda.activities.all().count() < 3 or microoda == self.object.microoda:
                        microodas.append(microoda.type.name)

                if len(microodas) > 0:
                    odas.append(oda)
                    microodas_list.append(microodas)
            if len(odas) > 0:
                odas_zip = zip(odas, microodas_list)
                odas_list.append(odas_zip)
                subjects_list.append(subject)

        subject_odas = zip(subjects_list, odas_list)

        context = super(UpdateMomentView, self).get_context_data(**kwargs)
        context.update({'moments_list': moments_list,
                        'tags': tags,
                        'subject_odas': subject_odas,
                        'moment_type_list': moment_type_list})
        print ('out get_context_data')
        return context

    def form_valid(self, form):
        print ("print update momento form")
        subject = self.request.POST.get('materia-list')
        oda = self.request.POST.get('oda-list')
        microoda = self.request.POST.get('micro-oda')
        moment_type = self.request.POST.get('tipo-momento')
        #h5p_url = self.request.POST.get('url_h5p')
        form.save_form(subject, oda, microoda, moment_type ) #, h5p_url)
        return redirect(to='momentos_view')


class DeleteMomentView(View):
    """
    Deletes Momento object
    """
    def dispatch(self, request, *args, **kwargs):
        Moment.objects.get(pk=self.kwargs['pk']).pre_delete()
        return redirect(to='momentos_view')


@method_decorator(xframe_options_exempt, name='dispatch')
class MomentView(DetailView):
    """
    Displays uploaded H5P package
    """
    template_name = 'packages/package_view.html'
    model = Moment
    context_object_name = 'package'

    def get_object(self, queryset=None):
        print ('in get object')
        if 'pk' in self.kwargs.keys():
            print (self.model.objects.get(pk=self.kwargs['pk']))
            return self.model.objects.get(pk=self.kwargs['pk'])   
        else:
            raise ValueError('Neither pk nor moment_id were given as parameters')

    
