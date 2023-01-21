#%%
import pandas as pd
import scipy.stats as stats
import numpy as np
from matplotlib import pyplot as plt
import tableone
# from zio_raw_config import ()
from utils import trimandlower
import seaborn as sns
import tableone 

PATH = "../"
DATA = "data/"

review_df = pd.read_csv(PATH+\
        DATA+'zio_raw.csv',
        # encoding="ISO-8859-1"
        )

review_df = trimandlower(review_df)
#%%

cols_i_want = [
    # 'division_fcdmd', 'primaryrequesttypeview2', 'classificationview2',
    # 'servicenameview2', 
    'cprsstatus', 
    # 'fileentrydatetime2',
    # 'requestdatetime2', 'earliestdate2', 'elapseddaysfromfileentrydate2',
    # 'elapseddaysfrompatientindicateddate2', 'covidpriority', 'urgencycat',
    # 'patientname', 'patientssn2', 'eligibility', 'phoneresidence',
    # 'phonecellular', 'streetaddress1', 'streetaddress2', 'city',
    # 'countyname', 'state', 'zip1', 'age', 'dateofbirth', 'dateofdeath',
    # 'pactteam', 'fromsta6a2', 'sendinglocationname2', 
    'fromstopcode2',
    # 'orderingprovider2', 
    'provisionaldiagnosis', 
    # 'provisionaldiagnosiscode',
    # 'displaytextofitemordered', 'completedate', 'tostopcode',
    # 'requestservicestopcode', 'appointmentprimarystopcode',
    # 'appointmentlocation', 'appointmentcreatedatetime',
    # 'desiredappointmentdate1', 'appointmentdatetime', 'appointmentstatus',
    # 'documentlocationname', 'firstactivedatetime', 'firstscheduleddatetime',
    # 'daysfromfirstactivetofirstscheduled', 'firstcompletedatetime',
    # 'firstforwardedfromdatetime', 'firstforwardedfromservicename',
    # 'daysfromfileentrytofirstforwardedfrom', 'lastactiondate',
    # 'dayssincelastactivity', 'lastactiontaken',
    # 'lastknownactivityenteredbystaff', 'lastknownactivitycomment',
    # 'communitycareprogramname', 'commcareprovider1', 'call11', 'call21',
    # 'call31', 'letter1', 'unschedulednoactivitygt14days',
    # 'unschedulednoactivitygt30days', 'opengt30daysfromearliestdate',
    # 'opengt90daysfromearliestdate', 'opengt365daysfromearliestdate',
    # 'statopengt48hours', 'pendinggt2businessdays', 'partial10days',
    # 'linktopastappt', 'schednotlinked', 'rctexpected', 'rct',
    # 'canscore90days', 'consultsid2', 'consultien2'
    ]

prov_dx_labels = {
    'unspecified_atrial_fibrillation':'af', 
    'chronic_atrial_fibrillation,_unspecified':'af', 
    'longstanding_persistent_atrial_fibrillation':'af', 
    'paroxysmal_atrial_fibrillation':'af',
    'other_persistent_atrial_fibrillation':'af', 
    # 'syncope_and_collapse', 
    'unspecified_atrial_flutter':'af', 
    # 'encounter_for_general_adult_medical_examination_with_abnormal_findings', 
    # 'bradycardia,_unspecified', 'tachycardia,_unspecified', 
    # 'essential_(primary)_hypertension', 'muscle_weakness_(generalized)', 
    # 'dizziness_and_giddiness', 'shortness_of_breath', 
    # 'encounter_for_screening_for_cardiovascular_disorders', 
    'cerebral_infarction,_unspecified':'cva', 
    # 'ventricular_premature_depolarization', 
    'permanent_atrial_fibrillation':'af',
    # 'ventricular_tachycardia', 
    # 'hypotension,_unspecified', 'diplopia', 
    # 'dyspnea,_unspecified', 'orthostatic_hypotension', 
    'palpitations':'palpitations', 
    'typical_atrial_flutter':'af', 
    # 'heat_syncope,_initial_encounter', 
    # 'supraventricular_tachycardia', 
    'cardiac_arrhythmia,_unspecified':'unspecified', 
    'atypical_atrial_flutter':'af', 
    # 'unspecified_systolic_(congestive)_heart_failure', 
    # 'abnormal_electrocardiogram_[ecg]_[ekg]', 
    # 'nonrheumatic_aortic_(valve)_insufficiency', 
    # 'atherosclerotic_heart_disease_of_native_coronary_artery_without_angina_pectoris',
    'cerebellar_stroke_syndrome':'cva', 
    # 'left_posterior_fascicular_block', 
    # 'paroxysmal_tachycardia,_unspecified', 
    'cerebral_ischemia':'cva', 
    'cerebrovascular_disease,_unspecified':'cva', 
    # 'other_fatigue', 'obstructive_hypertrophic_cardiomyopathy', 
    # 'chronic_systolic_(congestive)_heart_failure', 
    'amaurosis_fugax':'embolic_event', 
    'central_retinal_artery_occlusion,_right_eye':'embolic_event', 
    # 'other_forms_of_chronic_ischemic_heart_disease', 
    # 'altered_mental_status,_unspecified', 
    # 'fall_on_same_level_from_slipping,_tripping_and_stumbling_without_subsequent_striking_against_object,_initial_encounter', 
    'unspecified_abnormalities_of_heart_beat':'unspecified', 
    # 'other_specified_heart_block', 
    'transient_cerebral_ischemic_attack,_unspecified':'cva', 
    # 'bifascicular_block', 'left_bundle-branch_block,_unspecified', 
    # 'other_restrictive_cardiomyopathy', 
    'other_cerebrovascular_disease':'cva', 
    # 'edema,_unspecified', 'chest_pain,_unspecified', 
    'other_sequelae_of_cerebral_infarction':'cva', 
    # 'low_vision,_one_eye,_unspecified_eye', 
    'cerebral_infarction_due_to_unspecified_occlusion_or_stenosis_of_left_middle_cerebral_artery':"cva", 
    'other_transient_cerebral_ischemic_attacks_and_related_syndromes':'cva', 
    # 'unilateral_primary_osteoarthritis,_right_knee', 
    'cerebral_infarction_due_to_embolism_of_unspecified_anterior_cerebral_artery':'cva', 
    # 'nonrheumatic_mitral_(valve)_insufficiency', 
    'other_specified_cardiac_arrhythmias':'unspecified', 
    'central_retinal_artery_occlusion,_left_eye':'embolic_event', 
    # 'fall_from_chair,_subsequent_encounter', 
    'brain_stem_stroke_syndrome':'cva', 
    # 'other_fall_on_same_level,_initial_encounter', 'unspecified_right_bundle-branch_block', 
    # 'localized_edema', 'atrioventricular_block,_second_degree', 
    # 'chronic_total_occlusion_of_coronary_artery', 
    'aphasia':'cva', 'vascular_parkinsonism':'cva', 
    'memory_deficit_following_other_cerebrovascular_disease':'cva', 
    # 'unilateral_primary_osteoarthritis,_right_hip', 
    # 'other_nontraumatic_intracerebral_hemorrhage', 
    'retinal_artery_branch_occlusion,_right_eye':'embolic event', 
    # 'unspecified_retinal_disorder', 
    'personal_history_of_transient_ischemic_attack_(tia),_and_cerebral_infarction_without_residual_deficits':'cva', 
    # 'pre-excitation_syndrome', 'other_fall_on_same_level,_subsequent_encounter', 
    'family_history_of_stroke':'cva', 
    # 'nausea', 'atrial_premature_depolarization', 'other_chest_pain', 'other_visual_disturbances', 
    # 'cardiac_murmur,_unspecified', 'atherosclerosis_of_coronary_artery_bypass_graft(s)_without_angina_pectoris', 
    # 'myotonic_muscular_dystrophy', 
    'other_cerebral_infarction':'cva', 
    'cerebral_infarction_due_to_unspecified_occlusion_or_stenosis_of_cerebral_arteries':'cva', 
    # 'st_elevation_(stemi)_myocardial_infarction_involving_left_anterior_descending_coronary_artery', 
    'unspecified_retinal_vascular_occlusion':'embolic_event', 
    # 'angina_pectoris,_unspecified', 'other_right_bundle-branch_block', 
    'retinal_artery_branch_occlusion,_unspecified_eye':'embolic_event', 
    # 'non-st_elevation_(nstemi)_myocardial_infarction', 'fall_on_same_level_from_slipping,_tripping_and_stumbling_with_subsequent_striking_against_unspecified_object,_initial_encounter', 'other_specified_counseling', 
    'unqualified_visual_loss,_left_eye,_normal_vision_right_eye':'embolic_event', 
    # 'dyslexia_and_alexia', 'stress,_not_elsewhere_classified', 
    # 'systemic_sclerosis_with_lung_involvement', 
    'embolism_and_thrombosis_of_other_arteries':'embolic_event', 
    'cerebral_atherosclerosis':"cva", 
    'unspecified_sequelae_of_unspecified_cerebrovascular_disease':'cva', 
    'unspecified_sequelae_of_cerebral_infarction':'cva', 
    # 'other_peripheral_vertigo,_unspecified_ear', 
    'cerebral_infarction_due_to_embolism_of_unspecified_middle_cerebral_artery':'cva', 
    # 'nontraumatic_intracerebral_hemorrhage,_unspecified', 
    'cerebral_infarction_due_to_thrombosis_of_unspecified_cerebral_artery':'cva', 
    # 'carotid_sinus_syncope', 'low_back_pain', 
    'cerebral_infarction_due_to_thrombosis_of_right_middle_cerebral_artery':'cva', 
    # 'chronic_diastolic_(congestive)_heart_failure', 
    'transient_alteration_of_awareness':'cva', 
    # 'unspecified_fall,_initial_encounter', 'chronic_pulmonary_embolism', 'counseling,_unspecified', 
    # 'fall_(on)_(from)_unspecified_stairs_and_steps,_initial_encounter', 
    # 'sick_sinus_syndrome', 
    'cerebral_infarction_due_to_unspecified_occlusion_or_stenosis_of_other_cerebral_artery':'cva', 
    # 'unspecified_fall,_sequela', 'wild-type_transthyretin-related_(attr)_amyloidosis', 
    # 'atrial_septal_defect', 'pain_in_left_hip', 
    'monoplegia_of_upper_limb_following_unspecified_cerebrovascular_disease_affecting_right_dominant_side':'cva', 
    # 'other_heart_failure', 'other_nonrheumatic_aortic_valve_disorders', 
    # 'nonrheumatic_aortic_(valve)_stenosis', 'acute_systolic_(congestive)_heart_failure', 
    'vertigo_of_central_origin':'cva', 
    'cerebral_infarction_due_to_thrombosis_of_left_anterior_cerebral_artery':'cva', 
    # 'heart_failure,_unspecified', 'dilated_cardiomyopathy', 
    # 'other_hypertrophic_cardiomyopathy', 'isolated_myocarditis', 
    # 'atrioventricular_block,_complete', 
    # 'unspecified_atrioventricular_block', 'myocarditis,_unspecified', 
    # 're-entry_ventricular_arrhythmia', 'other_atrioventricular_block'
}

stopcodedic = {
    -1:'acute',130:'ED',
}
review_df = review_df[cols_i_want]
# review_df.columns = [col_replace_dic[item] for item in cols_i_want]

#%%
# remove incomplete consults:
review_df = review_df[review_df['cprsstatus'] == 'complete']
# remove generic reasons on provisional dx:
review_df = review_df[review_df['provisionaldiagnosis'] != 'encounter_for_screening_for_cardiovascular_disorders']


#%%
# fix all y/n cols:
# for col in y_n_cols:
#         review_df[col] = review_df[col].map(y_n_dic)
review_df['provisionaldiagnosis'] = review_df['provisionaldiagnosis'].map(prov_dx_labels).fillna('other')
review_df['fromstopcode2'] = review_df['fromstopcode2'].map(stopcodedic).fillna('outpatient')



# %%
review_df.to_csv(PATH+DATA+'zio_raw_trimmed.csv')
#%%
# Table one:
t1cols = ['age', 
        # 'study_reason', 
        'ord_prov', 'ord_notified',
       'who_notified',# 'results_date', 'notification_date',
       'notification_means', 'new_af', 
#        'other_findings',
       'change_rec', 'cards_contacted',
       'time_to_notification',
       ]
t1cat = [
        # 'study_reason', 
        'ord_prov', 'ord_notified',
       'who_notified','notification_means', 'new_af', 
       'change_rec', 'cards_contacted'
       ]

mytable = tableone.TableOne(review_df, columns=t1cols, categorical=t1cat, 
        # groupby=groupby, nonnormal=nonnormal, rename=labels, pval=False
        )
print(mytable.tabulate(
        # tablefmt = "fancy_grid"
        ))
