from __future__ import print_function
import os
import sys

def call_face_reco_script():
    os.system("sh bash_image_recog.sh")

def recognized_name_from_face(final_cust_id):
    import billing_details_testing_face
    billing_details_testing_face.bill_detail_main2(final_cust_id)

def intermediate_face_recog(names):
    import billing_details_testing_face
    #print("len of names: ",len(names))
    
    try:
        final_cust_id = billing_details_testing_face.recognised_customers(names)[0]

    except IndexError:
        final_cust_id = []

    #print("Customer Id in recognize module is: ", final_cust_id)
    recognized_name_from_face(final_cust_id)
    



