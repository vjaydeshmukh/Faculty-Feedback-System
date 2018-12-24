from django.shortcuts import render, redirect, HttpResponse
from .models import Feedback, UserProfile, TeacherProfile, Subject
from .forms import UserForm, UserProfileForm, TeacherProfileForm
from .filters import TeacherProfileFilter
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import json
# Create your views here.


def index(request):
    if request.user.is_authenticated():
        if TeacherProfile.objects.all().filter(user=request.user).count() == 0:
            f = Feedback.objects.filter(student=UserProfile.objects.filter(user=request.user))
            subjects_done_feedback = [i.subject.name for i in f]
            username = request.user
            u = UserProfile.objects.filter(user=username)
            fname = u[0].fname
            lname = u[0].lname
            subject_list = [i.name for i in u[0].subject.all()]
            teacher_list = TeacherProfile.objects.all()
            for i in subject_list:
                if i in subjects_done_feedback:
                    try:   
                        subject_list.remove(i)
                    except ValueError:
                        pass
            print(subject_list)
            # teacher_filtered = TeacherProfileFilter(request.GET, queryset=teacher_list)
            if request.POST:
                u = u[0]
                s = request.POST.get('subject')
                # fname = request.POST.get('fname')
                # lname = request.POST.get('lname')
                t = request.POST.get('teacher')
                f1 = request.POST.get('f1')
                f2 = request.POST.get('f2')
                f3 = request.POST.get('f3')
                f4 = request.POST.get('f4')
                f5 = request.POST.get('f5')
                f6 = request.POST.get('f6')
                f7 = request.POST.get('f7')
                f8 = request.POST.get('f8')
                f9 = request.POST.get('f9')
                sug = request.POST.get('sug')
                tea = TeacherProfile.objects.filter(fname=t.split(" ")[0])
                print(tea)
                sub = Subject.objects.filter(name=s)
                print(sub)
                f = Feedback.objects.create(
                    student=u,
                    subject=sub[0],
                    teacher=tea[0],
                    res1=f1,
                    res2=f2,
                    res3=f3,
                    res4=f4,
                    res5=f5,
                    res6=f6,
                    res7=f7,
                    res8=f8,
                    res9=f9,
                    sug=sug
                )
                f.save()
                # s = request.POST.get('subject')
                return redirect('analytics')
            context = {
                'fname': fname,
                'lname': lname,
                'teacher_list': teacher_list,
                'subject_list': subject_list
            }
            return render(request, 'appOne/dashboard.html', context)
        else:
            return redirect('teacher_analytics')
    else:
        return redirect('signup')



def analytics(request):
    #To be integrated with the frontend and to get the list of subjects dynamically for particular student
    #depending upon the semester.

    if Feedback.objects.all().count() != 0:
        subject_list = []
        avg_sub = []
        if request.user.is_authenticated():
            user = request.user
            student = UserProfile.objects.filter(user=user)
            subjects = [i.name for i in student[0].subject.all()]
            for subject in subjects:
                sub_obj = Subject.objects.filter(name=subject)
                if Feedback.objects.filter(subject=sub_obj).count() != 0:
                    student = UserProfile.objects.filter(user=request.user)
                    sub = Feedback.objects.filter(subject=sub_obj, student=student)
                    print(sub)
                    sum = 0
                    sum = sub[0].res1 / 5 + sub[0].res2 / 5  + sub[0].res3 / 5 + sub[0].res4 / 5 + sub[0].res5 / 5 + sub[0].res6 / 5 + sub[0].res7 / 5 + sub[0].res8 / 5 + sub[0].res9 / 5
                    avg = sum / 9
                    avg_sub.append(round(avg * 100))
                    # sum_sub = 0
                    # for i in range(0, len(avg_sub)):
                    #     sum_sub += avg_sub[i]
                    # print(avg_sub)
                    # av_sub = sum_sub / len(avg_sub)
                    # print(av_sub)
                    # final.append(int((av_sub / 5) * 100))
                    subject_list.append(subject)
                    print(avg_sub)
            context = {
                    'feedback': avg_sub,
                    'subject': subject_list,
                    'f': ''
                }
            print(context['subject'])
            return render(request, 'appOne/analytics.html', context)
        else:
            return redirect('signup')
    else:
        if request.user.is_authenticated():
            return render(request, 'appOne/analytics.html', {'f': 'No Fucks Yet!!'})
        else:
            return redirect('signup')


        # if request.user.is_authenticated():
        #     final = []
        #     subject = []
        #     # CALCULATIONS FOR AM3
        #     if Feedback.objects.all().filter(subject='Applied Mathematics - III', user=request.user).count() != 0:
        #         am3 = Feedback.objects.all().filter(subject='Applied Mathematics - III', user=request.user)
        #         avg_am3 = []
        #         for i in range(0, len(am3)):
        #             sum = 0
        #             sum = am3[i].res1 + am3[i].res2 + am3[i].res3 + am3[i].res4 + am3[i].res5 + am3[i].res6 + am3[i].res7 + am3[i].res8 + am3[i].res9
        #             avg = sum / 9
        #             avg_am3.append(avg)
        #         sum_am3 = 0
                # for i in range(0, len(avg_am3)):
                #     sum_am3 += avg_am3[i]
                # av_am3 = sum_am3 / len(avg_am3)
                # print(av_am3)
                # final.append(int((av_am3 / 5) * 100))
                # subject.append('AM3')

        #     # CALCULATIONS FOR AOA
        #     if Feedback.objects.all().filter(subject='Analysis of Algorithms', user=request.user).count() != 0:
        #         aoa = Feedback.objects.all().filter(subject='Analysis of Algorithms', user=request.user)
        #         avg_aoa = []
        #         for i in range(0, len(aoa)):
        #             sum = 0
        #             sum = aoa[i].res1 + aoa[i].res2 + aoa[i].res3 + aoa[i].res4 + aoa[i].res5 + aoa[i].res6 + aoa[i].res7 + aoa[i].res8 + aoa[i].res9
        #             avg = sum / 9
        #             avg_aoa.append(avg)
        #         sum_aoa = 0
        #         for i in range(0, len(avg_aoa)):
        #             sum_aoa += avg_aoa[i]
        #         av_aoa = sum_aoa / len(avg_aoa)
        #         print(av_aoa)
        #         final.append(int((av_aoa / 5) * 100))
        #         subject.append('AOA')

        #     # CALCULATIONS FOR coa
        #     if Feedback.objects.all().filter(subject='Computer Organization and Architecture', user=request.user).count() != 0:
        #         coa = Feedback.objects.all().filter(subject='Computer Organization and Architecture', user=request.user)
        #         avg_coa = []
        #         for i in range(0, len(coa)):
        #             sum = 0
        #             sum = coa[i].res1 + coa[i].res2 + coa[i].res3 + coa[i].res4 + coa[i].res5 + coa[i].res6 + coa[i].res7 + coa[i].res8 + coa[i].res9
        #             avg = sum / 9
        #             avg_coa.append(avg)
        #         sum_coa = 0
        #         for i in range(0, len(avg_coa)):
        #             sum_coa += avg_coa[i]
        #         av_coa = sum_coa / len(avg_coa)
        #         print(av_coa)
        #         final.append(int((av_coa / 5) * 100))
        #         subject.append('COA')

        #     # CALCULATIONS FOR cg
        #     if Feedback.objects.all().filter(subject='Computer Graphics', user=request.user).count() != 0:
        #         cg = Feedback.objects.all().filter(subject='Computer Graphics', user=request.user)
        #         avg_cg = []
        #         for i in range(0, len(cg)):
        #             sum = 0
        #             sum = cg[i].res1 + cg[i].res2 + cg[i].res3 + cg[i].res4 + cg[i].res5 + cg[i].res6 + cg[i].res7 + cg[i].res8 + cg[i].res9
        #             avg = sum / 9
        #             avg_cg.append(avg)
        #         sum_cg = 0
        #         for i in range(0, len(avg_cg)):
        #             sum_cg += avg_cg[i]
        #         av_cg = sum_cg / len(avg_cg)
        #         print(av_cg)
        #         final.append(int((av_cg / 5) * 100))
        #         subject.append('CG')

        #     # CALCULATIONS FOR os
        #     if Feedback.objects.all().filter(subject='Operating System', user=request.user).count() != 0:
        #         os = Feedback.objects.all().filter(subject='Operating System', user=request.user)
        #         avg_os = []
        #         for i in range(0, len(os)):
        #             sum = 0
        #             sum = os[i].res1 + os[i].res2 + os[i].res3 + os[i].res4 + os[i].res5 + os[i].res6 + os[i].res7 + os[i].res8 + os[i].res9
        #             avg = sum / 9
        #             avg_os.append(avg)
        #         sum_os = 0
        #         for i in range(0, len(avg_os)):
        #             sum_os += avg_os[i]
        #         av_os = sum_os / len(avg_os)
        #         print(av_os)
        #         final.append(int((av_os / 5) * 100))
        #         subject.append('OS')

        #     # CALCULATIONS FOR osl
        #     if Feedback.objects.all().filter(subject='Open Source Tech Lab', user=request.user).count() != 0:
        #         osl = Feedback.objects.all().filter(subject='Open Source Tech Lab', user=request.user)
        #         avg_osl = []
        #         for i in range(0, len(osl)):
        #             sum = 0
        #             sum = osl[i].res1 + osl[i].res2 + osl[i].res3 + osl[i].res4 + osl[i].res5 + osl[i].res6 + osl[i].res7 + osl[i].res8 + osl[i].res9
        #             avg = sum / 9
        #             avg_osl.append(avg)
        #         sum_osl = 0
        #         for i in range(0, len(avg_osl)):
        #             sum_osl += avg_osl[i]
        #         av_osl = sum_osl / len(avg_osl)
        #         print(av_osl)
        #         final.append(int((av_osl / 5) * 100))
        #         subject.append('OSL')

        #     # FINAL PYTHON LIST
        #     print(final)
        #     print(subject)
            # context = {
            #     'feedback': final,
            #     'subject': subject,
            #     'f': ''
            # }
        #     return render(request, 'appOne/analytics.html', context)
        # else:
        #     return redirect('signup')



def teacher_analytics(request):
    #To be integrated with the frontend and to get the list of subjects dynamically for particular teacher
    #depending upon the semester.

    if Feedback.objects.all().count() != 0:
        avg_sub = []
        subject_list = []
        if request.user.is_authenticated():
            user = request.user;
            teacher = TeacherProfile.objects.filter(user=user)
            subjects = [i.name for i in teacher[0].subject.all()]
            print(teacher[0].fname + " " + teacher[0].lname)
            fname = teacher[0].fname
            lname = teacher[0].lname
            for subject in subjects:
                sub_obj = Subject.objects.filter(name=subject)
                if Feedback.objects.filter(subject=sub_obj).count() != 0:
                    teacher = TeacherProfile.objects.filter(user=request.user)
                    sub = Feedback.objects.filter(subject=sub_obj, teacher=teacher)
                    print(sub)
                    sum = 0
                    sum = sub[0].res1 / 5 + sub[0].res2 / 5  + sub[0].res3 / 5 + sub[0].res4 / 5 + sub[0].res5 / 5 + sub[0].res6 / 5 + sub[0].res7 / 5 + sub[0].res8 / 5 + sub[0].res9 / 5
                    avg = sum / 9
                    avg_sub.append(round(avg * 100))
                    # sum_sub = 0
                    # for i in range(0, len(avg_sub)):
                    #     sum_sub += avg_sub[i]
                    # print(avg_sub)
                    # av_sub = sum_sub / len(avg_sub)
                    # print(av_sub)
                    # final.append(int((av_sub / 5) * 100))
                    subject_list.append(subject)
                    print(avg_sub)
            context = {
                    'feedback': avg_sub,
                    'subject': subject_list,
                    'fname': fname,
                    'lname': lname,
                    'f': ''
                }
            return render(request, 'appOne/teacher_analytics.html', context)
        else:
            return redirect('signup')
    else:
        if request.user.is_authenticated():
            return render(request, 'appOne/teacher_analytics.html', {'f': 'No Fucks Yet!!'})
        else:
            return redirect('signup')





        # if request.user.is_authenticated():
        #     username = request.user
        #     u = TeacherProfile.objects.all().filter(user=username)
        #     print(u[0].fname + " " + u[0].lname)
        #     fname = u[0].fname
        #     lname = u[0].lname
        #     final = []
        #     subject = []
        #     # CALCULATIONS FOR AM3
        #     if Feedback.objects.all().filter(subject='Applied Mathematics - III', fname=fname, lname=lname).count() != 0:
        #         am3 = Feedback.objects.all().filter(subject='Applied Mathematics - III', fname=fname, lname=lname)
        #         print(am3)
        #         avg_am3 = []
        #         for i in range(0, len(am3)):
        #             sum = 0
        #             sum = am3[i].res1 + am3[i].res2 + am3[i].res3 + am3[i].res4 + am3[i].res5 + am3[i].res6 + am3[i].res7 + am3[i].res8 + am3[i].res9
        #             avg = sum / 9
        #             avg_am3.append(avg)
        #         sum_am3 = 0
        #         for i in range(0, len(avg_am3)):
        #             sum_am3 += avg_am3[i]
        #         av_am3 = sum_am3 / len(avg_am3)
        #         print(av_am3)
        #         final.append(int((av_am3 / 5) * 100))
        #         subject.append('AM3')

        #     # CALCULATIONS FOR AOA
        #     if Feedback.objects.all().filter(subject='Analysis of Algorithms', fname=fname, lname=lname).count() != 0:
        #         aoa = Feedback.objects.all().filter(subject='Analysis of Algorithms', fname=fname, lname=lname)
        #         avg_aoa = []
        #         for i in range(0, len(aoa)):
        #             sum = 0
        #             sum = aoa[i].res1 + aoa[i].res2 + aoa[i].res3 + aoa[i].res4 + aoa[i].res5 + aoa[i].res6 + aoa[i].res7 + aoa[i].res8 + aoa[i].res9
        #             avg = sum / 9
        #             avg_aoa.append(avg)
        #         sum_aoa = 0
        #         for i in range(0, len(avg_aoa)):
        #             sum_aoa += avg_aoa[i]
        #         av_aoa = sum_aoa / len(avg_aoa)
        #         print(av_aoa)
        #         final.append(int((av_aoa / 5) * 100))
        #         subject.append('AOA')
        #     # CALCULATIONS FOR coa
        #     if Feedback.objects.all().filter(subject='Computer Organization and Architecture', fname=fname, lname=lname).count() != 0:
        #         coa = Feedback.objects.all().filter(subject='Computer Organization and Architecture', fname=fname, lname=lname)
        #         avg_coa = []
        #         for i in range(0, len(coa)):
        #             sum = 0
        #             sum = coa[i].res1 + coa[i].res2 + coa[i].res3 + coa[i].res4 + coa[i].res5 + coa[i].res6 + coa[i].res7 + coa[i].res8 + coa[i].res9
        #             avg = sum / 9
        #             avg_coa.append(avg)
        #         sum_coa = 0
        #         for i in range(0, len(avg_coa)):
        #             sum_coa += avg_coa[i]
        #         av_coa = sum_coa / len(avg_coa)
        #         print(av_coa)
        #         final.append(int((av_coa / 5) * 100))
        #         subject.append('COA')

        #     # CALCULATIONS FOR cg
        #     if Feedback.objects.all().filter(subject='Computer Graphics', fname=fname, lname=lname).count() != 0:
        #         cg = Feedback.objects.all().filter(subject='Computer Graphics', fname=fname, lname=lname)
        #         avg_cg = []
        #         for i in range(0, len(cg)):
        #             sum = 0
        #             sum = cg[i].res1 + cg[i].res2 + cg[i].res3 + cg[i].res4 + cg[i].res5 + cg[i].res6 + cg[i].res7 + cg[i].res8 + cg[i].res9
        #             avg = sum / 9
        #             avg_cg.append(avg)
        #         sum_cg = 0
        #         for i in range(0, len(avg_cg)):
        #             sum_cg += avg_cg[i]
        #         av_cg = sum_cg / len(avg_cg)
        #         print(av_cg)
        #         final.append(int((av_cg / 5) * 100))
        #         subject.append('CG')

        #     # CALCULATIONS FOR os
        #     if Feedback.objects.all().filter(subject='Operating System', fname=fname, lname=lname).count() != 0:
        #         os = Feedback.objects.all().filter(subject='Operating System', fname=fname, lname=lname)
        #         avg_os = []
        #         for i in range(0, len(os)):
        #             sum = 0
        #             sum = os[i].res1 + os[i].res2 + os[i].res3 + os[i].res4 + os[i].res5 + os[i].res6 + os[i].res7 + os[i].res8 + os[i].res9
        #             avg = sum / 9
        #             avg_os.append(avg)
        #         sum_os = 0
        #         for i in range(0, len(avg_os)):
        #             sum_os += avg_os[i]
        #         av_os = sum_os / len(avg_os)
        #         print(av_os)
        #         final.append(int((av_os / 5) * 100))
        #         subject.append('OS')

        #     # CALCULATIONS FOR osl
        #     if Feedback.objects.all().filter(subject='Open Source Tech Lab', fname=fname, lname=lname).count() != 0:
        #         osl = Feedback.objects.all().filter(subject='Open Source Tech Lab', fname=fname, lname=lname)
        #         avg_osl = []
        #         for i in range(0, len(osl)):
        #             sum = 0
        #             sum = osl[i].res1 + osl[i].res2 + osl[i].res3 + osl[i].res4 + osl[i].res5 + osl[i].res6 + osl[i].res7 + osl[i].res8 + osl[i].res9
        #             avg = sum / 9
        #             avg_osl.append(avg)
        #         sum_osl = 0
        #         for i in range(0, len(avg_osl)):
        #             sum_osl += avg_osl[i]
        #         av_osl = sum_osl / len(avg_osl)
        #         print(av_osl)
        #         final.append(int((av_osl / 5) * 100))
        #         subject.append('OSL')

        #     # FINAL PYTHON LIST
        #     print(final)
        #     print(subject)
        #     context = {
        #         'feedback': final,
        #         'subject': subject,
        #         'fname': fname,
        #         'lname': lname,
        #         'f': ''
        #     }
        #     return render(request, 'appOne/teacher_analytics.html', context)
        # else:
        #     return redirect('signup')
    # else:
    #     if request.user.is_authenticated():
    #         return render(request, 'appOne/teacher_analytics.html', {'f': 'No Feedbacks Yet!!'})
    #     else:
    #         return redirect('signup')
def get_teacher_name(request, subject):
    s = Subject.objects.filter(name=subject)
    if s.count() != 0:
        t = TeacherProfile.objects.filter(subject=Subject.objects.filter(name=subject)[0])
        teacher_names = [i.fname + ' ' + i.lname for i in t]
    else:
        teacher_names = ['No Teacher Found']
    print(teacher_names)
    return HttpResponse(json.dumps({'teacher_names': teacher_names}), content_type="application/json")


def teacherSignup(request):

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        teacher_form = TeacherProfileForm(data=request.POST)

        if user_form.is_valid() and teacher_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            teacher = teacher_form.save(commit=False)
            teacher.user = user
            teacher.save()
            login(request, user)
            return redirect('teacher_analytics')
    else:
        user_form = UserForm()
        teacher_form = TeacherProfileForm()
    return render(request, 'appOne/teacher_signup.html', {'user_form': user_form,
                                                          'teacher_form': teacher_form})


def signup(request):

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('index')
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'appOne/signup.html', {'user_form': user_form,
                                                  'profile_form': profile_form})


@login_required
def logOut(request):
    logout(request)
    return redirect('signup')


def teacherLogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('teacher_analytics')
        else:
            return render(request, 'appOne/teacher_login.html', {'i': 'Invalid Password/SAP ID'})
    return render(request, 'appOne/teacher_login.html', {'i': ''})


def logIn(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username)
        try:
            u = UserProfile.objects.all().filter(user=user)
        except:
            print("User does not exist!")
        if(u.count() == 0):
            return render(request, 'appOne/login.html', {'i': 'Invalid Password/SAP ID'})
        user = authenticate(username=username, password=password)

        if user and (u.count() != 0):
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'appOne/login.html', {'i': 'Invalid Password/SAP ID'})
    return render(request, 'appOne/login.html', {'i': ''})
