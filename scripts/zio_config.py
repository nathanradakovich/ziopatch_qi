cols_i_want = [
      'city', 
      'state', 
      'age', 
      # 'provisionaldiagnosis',
      # 'provisionaldiagnosiscode', 'dx_code_on_final_report',
      'reason_for_study', 
      'who_was_ordering_provider_(pcp,_ed,_cards,_neuro)',
      'did_ordering_provider_notify_patient', 
      'if_not,_who_notified_pt',
      'date_final_results_published', 
      'date_pt_notified',
      'how_was_pt_notified', 
      'new_af', 
      'other_significant_findings',
      'was_the_consult_question_clearly_answered_on_interpretation_or_summary?',
      'recommendation_provided_(change_to_care_plan_suggested)',
      'did_cardiologist_contact_ordering_provider_directly', 
      # 'notes',
      # 'dx_code'
]

col_replace_dic = {
   'city':'city', 
   'state':'state', 
   'age':'age', 
   # 'provisionaldiagnosis',
   # 'provisionaldiagnosiscode', 'dx_code_on_final_report',
   'reason_for_study':'study_reason', 
   'who_was_ordering_provider_(pcp,_ed,_cards,_neuro)':'ord_prov',
   'did_ordering_provider_notify_patient':'ord_notified', 
   'if_not,_who_notified_pt':'who_notified',
   'date_final_results_published':'results_date', 
   'date_pt_notified':'notification_date',
   'how_was_pt_notified':'notification_means', 
   'new_af':'new_af', 
   'other_significant_findings':'other_findings',
   'was_the_consult_question_clearly_answered_on_interpretation_or_summary?':'question_answered',
   'recommendation_provided_(change_to_care_plan_suggested)':'change_rec',
   'did_cardiologist_contact_ordering_provider_directly':'cards_contacted', 
   # 'notes',
   # 'dx_code'
   }

prov_dic = {
'pcp':'pcp', 'ed':'acute', 'cardiology':'cards', 'er':'acute', 'inpatient':'acute',
       'inpatient_cardiology':'cards', 'neuro':'acute', 'ct_surg':'acute'
}
y_n_dic = {'no':'n', '*no_(see_notes)_':'n', 'yes':'y','yes_(tagged_on_report)':'y',
       'no_(unclear_how_results_were_conveyed)_':'n','unclear':'n',
       }
y_n_cols = ['ord_notified','new_af','question_answered',
        'change_rec', 'cards_contacted']
notification_dic = {
        'pt_called_to_ask_about_results_3/30/20':'phone',
       'does_not_appear_to_have_been_notified':'n',
       'in_scheduled_cardiology_appointment':'appointment', 'letter':'letter',
       'telephone_visit_with_pcp':'phone', 'pcp_visit':'appointment', 'cardiology_visit':'appointment',
       'er_visit_':'other', 'unclear':'other'
}
notifier_dic = {
        'cardiology':'cards', 'does_not_appear_to_have_been_notified':'n',
        'pcp':'pcp',
       'outpatient_cardiology':'pcp', 'er_(separate_visit)':'other', 'unclear':'n',
       'no_one':'n', 'n/a':'n', 'seen_in-patient':'other',
       'discussed_at_cardiology_visit':'cards',
       'patient_called,_spoke_to_cardiology':'cards', 'pact_rn':'pcp',
       'another_member_of_ct_surg_team':'other'
}
reason_dic = {
        'syncope':'syncope', 'aflutter':'af', 
        'bradycardia_vs_afib':'bradycardia', 'tachy_brady':'bradycardia',
       'afib':'af',
       '82_y/o_male_with_afib.__had_episode_of_generalized_weakness_about_6_mo_\nago_that_lasted_a_few_hours._ziopatch_to_evaluate_for_possible_episodic_bradycardia/tachycardi.':'af',
       'dyspnea_and_presyncope':'dyspnea', 'palpitations':'palpitations',
       'ventricular_ectopy':'pvc', 'svt':'tachycardia', 
       'history_of_heart_flutter':'af', 'chf':'hf',
       'av_block':'heart_block', 
       'sinus/junctional_bradycardia':'tachycardia', 
       'irregular_heart_beat':'palpitations',
       'pvcs':'pvc', 'eval_for_af_burden,_h/o_afib':'af',
       'eval_for_af_burden_and_rates,_h/o_afib_with_slow_ventricular_response_and_some_occasional_dizziness':'af',
       'new_afib,_eval_rate_control':'af', 'paf,_eval_for_afib':'af',
       'eval_bradycardia':'bradycardia',
       'afib/flutter_and_vt_versus_bbb_aberrancy_on_last_zio;_pls_re-evaluate_rate':'af',
       'paf_with_tachycardia':'af', 'post-cva_afib_assessment':'cva',
       'eval_afib_rate':'af', 'eval_afib_burden':'af', 'f/u_after_ablation':'af',
       'f/u_for_new_diagnosis_afib':'af', 'post_afib_ablation':'af', 'paf_and_cva':'cva',
       'afib_with_fall':'af', 'cad_s/p_fall_with_tte_showing_new_afib':'af',
       'dizziness,_bradycardia,_h/o_afl':'bradycardia', 'abnormal_ecg':'other',
       'eval_of_rate_control':'af'
}
