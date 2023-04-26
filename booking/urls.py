from django.urls import path, re_path
from .views import *


urlpatterns = [
    path('requestbooking/',AddBooking.as_view()),
    path('insertLeads/', InsertLeads.as_view()),

    # path('getbookings/<int:page_no>/',GetBookings.as_view()),
    path('assingbooking/',AssignBooking.as_view()),
    path('confirmbooking/',ConfirmBooking.as_view()),
    path('addagent/',AddAgent.as_view()),
    path('updateagent/',UpdateAgent.as_view()),
    path('contactus/',Contact.as_view()),
    path('getcontact/<int:page_no>/',ContactMessages.as_view()),
    path('getpaymentdetail/',GetPayment.as_view()),
    path('postpayment/',Payment.as_view()),
    path('partialpayment/',PartialPayment.as_view()),
    path('addleads/',AddLeads.as_view()),
    path('getleads/<int:page_no>/',LeadsDetail.as_view()),
    path('testbooking/<int:page_no>/',TestBooking.as_view()),
    path('lockcontact/',LockContact.as_view()),
    path('allowpartiis_okalpayment/',PartialAllowPayment.as_view()),
    path('jtrackerbookin/',JSaveBooking.as_view()),
    path('getJtrackerbookings/<int:page_no>/',GetJtrackerBookings.as_view()),

    path('saveagreemnt/',SaveAgreement.as_view()),
    path('getagreement/<int:page_no>/',GetAgreements.as_view()),

    path('savecarieeragreemnt/',SaveCarrierAgreeent.as_view()),
    path('getcarieeragreement/<int:page_no>/',GetCarrierAgreements.as_view()),

    path('saverefundagreemnt/',SaveRefundAgreement.as_view()),
    path('getrefundagreement/<int:page_no>/',GetRefundAgreements.as_view()),

    path('saveLeadwithText/',SaveTextLeads.as_view()),
    path('updatelead/<int:lead_id>/',UpdateLeads.as_view()),

    # path('generateinvoice/<int:lead_id>/', GenerateInvoice.as_view()),
    # path('detaillead/<str:lead_id>/', DetailLead.as_view()),

    path('deleteLead/<int:lead_id>/',DeleteLead.as_view()),
    path('getuserrole/',GetUserRole.as_view()),

######################Important Apis To Test and working################
    path('bulkassing/', BulkAssingtoAgent.as_view()),
    path('assignLead/',AssignedtoAgent.as_view()),
    path("getagentdetail/<int:id>/", GetAgentDetail.as_view()),
    path('getagent/', GetAgents.as_view()),
    path('getagentfast/', GetAgentsFast.as_view()),
    path("test_Search/<int:page_no>/", testSearch.as_view()),
    path("test_Search_New/<int:page_no>/", testSearch_new.as_view()),
    path('SearchFastNew/', SearchNewLeads.as_view()),

    ######################Important Apis To Test and working################


    path('getspecificagent321/<status_new>/',GetSpecificAgentLeads.as_view()),
    path('updateLeadStatus/',UpdateLeadStatus.as_view()),
    path('confirmLead/',ConfirmLeads.as_view()),
    path('sendEmails/',EmailsSend.as_view()),
    path('getConfirmBooking/<int:page_no>/',getConfirmLeads.as_view()),
    path('getYearMakeModel/',YearMakeModel.as_view()),
    path('sendcode/',PhoneVerification.as_view()),
    path('entercode/', EnterCode.as_view()),
    path('searchagents/<str:key>', SortAgents.as_view()),

]
