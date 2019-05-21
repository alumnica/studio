from alumnica_model.models import Moment, Tag
from alumnica_model.models.content import typeMoment, Subject, Content
from studio.forms.moment_forms import MomentCreateForm, MomentUpdateForm

def get_context_data(context, **kwargs):
    print ('create momentos')    
    print (kwargs)
    print (kwargs.get('name'))    
    
         
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
    context.update({'moments_list': moments_list,
                    'tags': tags,
                    'subject_odas': subject_odas,
                    'moment_type_list': moment_type_list}) 
    print (context)
    return context

def get_context_data_update(obj, context, **kwargs):
    moments_list = Moment.objects.all()
    tags = Tag.objects.all()
    moment_type_list = typeMoment.values()
    subjects_list = []
    odas_list = []

    for subject in Subject.objects.all():
        odas = []
        microodas_list = []

        if subject.ambit is not None:
            if obj.microoda is not None:
                if not subject.ambit.is_draft and obj.microoda.oda.subject != subject:
                    continue

        for oda in subject.odas.all():
            microodas = []
            for microoda in oda.microodas.all():
                if microoda.activities.all().count() < 3 or microoda == obj.microoda:
                    microodas.append(microoda.type.name)

            if len(microodas) > 0:
                odas.append(oda)
                microodas_list.append(microodas)
        if len(odas) > 0:
            odas_zip = zip(odas, microodas_list)
            odas_list.append(odas_zip)
            subjects_list.append(subject)

    subject_odas = zip(subjects_list, odas_list)    
    context.update({'moments_list': moments_list,
                    'tags': tags,
                    'subject_odas': subject_odas,
                    'moment_type_list': moment_type_list})
    return context

def form_valid(request, form):
    print (' valud save data after upload files ')    
    subject = request.POST.get('materia-list')
    oda = request.POST.get('oda-list')
    microoda = request.POST.get('micro-oda')
    moment_type = request.POST.get('tipo-momento')
    #if moment_type=='h5p':
    id_content = request.POST.get('id_content')
    print (moment_type)
    print (id_content)    

    form.save_form(request.user, subject, oda, microoda, moment_type, id_content) 
    return 
