'''
Created on Oct 22, 2015

@author: irma
'''
"""
import xlsxwriter,argparse,csv,os,math
import numpy as np

def create_workbook(csv_path,level):
    workbook = xlsxwriter.Workbook(os.path.join(csv_path,'results_'+str(level)+'.ods'),{'strings_to_numbers': True})

    exhaustive_max_column_width={}
    furer_max_column_width={}
    false_furer_max_column_width={}
    random_max_column_width={}
    worksheet = workbook.add_worksheet("exhaustive")
    embeddings_furer=[]
    embeddings_ffurer=[]
    embeddings_exhaustive=[]
    embeddings_random=[]
    
    avg_embeddings_furer=[]
    avg_embeddings_ffurer=[]
    avg_embeddings_random=[]
    
    std_embeddings_furer=[]
    std_embeddings_ffurer=[]
    std_embeddings_random=[]
    
    iteration_relError5_furer=[]
    iteration_relError5_ffurer=[]
    iteration_relError5_random=[]
    
    absError_furer={}
    absError_ffurer={}
    absError_random={}
    pattern_ids=[]
    
    #csv_file_exhaustive
    with open(os.path.join(csv_path,'exhaustive_'+str(level)+'.csv'), 'rb') as f:
        
        reader = csv.reader(f)
        emb_index=None
        for r, row in enumerate(reader):
            if r==0:
                emb_index=row.index("emb_120") 
            if r>0: 
               try:   
                  embeddings_exhaustive.append(float(row[emb_index]))
               except:
                   embeddings_exhaustive.append(None)
               
               pattern_ids.append(row[0])
            for c, col in enumerate(row):
                if(not c in exhaustive_max_column_width.keys()):
                    exhaustive_max_column_width[c]=0
                if(len(col)>exhaustive_max_column_width[c]):
                    exhaustive_max_column_width[c]=len(col)
                if not isinstance(col, str) and float(col):
                    worksheet.write_number(r, c, col)
                else:    
                    worksheet.write(r, c, col)
    for c in exhaustive_max_column_width.keys():
        worksheet.set_column(c,c, exhaustive_max_column_width[c]+2)
    worksheet.set_column(1,1, 20)
    
    worksheet1 = workbook.add_worksheet("furer_OBD")
    worksheet1_relError = workbook.add_worksheet("furer_OBD_RelError")
    
    #CSV furer-OBD
    with open(os.path.join(csv_path,'furer_'+str(level)+'.csv'), 'rb') as f:
        reader = csv.reader(f)
        initial_embedding_index=-1
        final_embedding_index=-1
        final_std_index=-1
        index_range_all_embeddings=[]
        
        for r, row in enumerate(reader):
            relErrorEmbeddings=[]
            if r==0:
                initial_embedding_index=row.index("emb_1")
                final_embedding_index=row.index("emb_120")
                final_std_index=row.index("std_120")
                index_range_all_embeddings=range(initial_embedding_index,final_embedding_index+1)
                worksheet1_relError.write(0,0,row[0])
                for i in range(1,120):
                    worksheet1_relError.write(0,i,'emb_'+str(i))
            if r>0:
               all_embeddings=[]
               for i in np.array(row)[np.array(index_range_all_embeddings)]:
                   if not i=='':
                      all_embeddings.append(float(i))
                   else:
                      all_embeddings.append(0)
               counter=0
               if len(embeddings_exhaustive)<r:
                       continue   
               for emb in all_embeddings:
                   n=None                
                   if embeddings_exhaustive[r-1]==0:
                       n=1
                   else:    
                       n=embeddings_exhaustive[r-1]
                   if n!=None and emb!=None:
                      relErrorEmbeddings.append(abs(emb-n)/n)
                   else:
                       relErrorEmbeddings.append(None)
               iteration=len(all_embeddings)
               for emb in all_embeddings:
                   counter+=1
                   if emb==None or n==None:
                       iteration=None
                       break
                   if (abs(emb-n)/n)*100<5:
                       iteration=counter
                       break
                       
               iteration_relError5_furer.append(iteration)
               avg_embeddings_furer.append(np.mean(np.array(all_embeddings)))
               if row[final_embedding_index]!='':
                  embeddings_furer.append(float(row[final_embedding_index])) #QUESTION: take average or final?
                  std_embeddings_furer.append(float(row[final_std_index]))
               else:
                  embeddings_furer.append(float(0)) #QUESTION: take average or final?
                  std_embeddings_furer.append(float(0))
            for c, col in enumerate(row):
                if(not c in furer_max_column_width.keys()):
                    furer_max_column_width[c]=0
                if(len(col)>furer_max_column_width[c]):
                    furer_max_column_width[c]=len(col)
                try:
                    if float(col):
                         worksheet1.write_number(r, c, col)
                    else:    
                         worksheet1.write(r, c, col)
                except:
                    worksheet1.write(r, c, col)
            col=1
            for e in relErrorEmbeddings:
                worksheet1_relError.write(r,col,e)
                col+=1
    for c in furer_max_column_width.keys():
        worksheet1.set_column(c,c, furer_max_column_width[c]+2)
    worksheet1.set_column(1,1, 20)
    worksheet1_relError.set_column(1,1, 20)
          
    #CSV furer-AD
    worksheet2 = workbook.add_worksheet("furer_AD")
    worksheet1_relError = workbook.add_worksheet("furer_AD_RelError")
    with open(os.path.join(csv_path,'Ffurer_'+str(level)+'.csv'), 'rb') as f:
        reader = csv.reader(f)
        initial_embedding_index=-1
        final_embedding_index=-1
        final_std_index=-1
        index_range_all_embeddings=[]
        for r, row in enumerate(reader):
            relErrorEmbeddings=[]
            if r==0:
                initial_embedding_index=row.index("emb_1")
                final_embedding_index=row.index("emb_120")
                final_std_index=row.index("std_120")
                index_range_all_embeddings=range(initial_embedding_index,final_embedding_index+1)
                worksheet1_relError.write(0,0,row[0])
                for i in range(1,120):
                    worksheet1_relError.write(0,i,'emb_'+str(i))
            if r>0:
               all_embeddings=[]
               for i in np.array(row)[np.array(index_range_all_embeddings)]:
                   if not i=='':
                      all_embeddings.append(float(i))
                   else:
                      all_embeddings.append(0)
               counter=0
               for emb in all_embeddings:
                   n=None
                   if embeddings_exhaustive[r-1]==0:
                       n=1
                   else:
                       n=embeddings_exhaustive[r-1]
                   if n!=None and emb!=None:
                      relErrorEmbeddings.append(abs(emb-n)/n)
                   else:
                       relErrorEmbeddings.append(None)
               iteration=len(all_embeddings)
               for emb in all_embeddings:
                   counter+=1
                   if emb==None or n==None:
                       iteration=None
                       break
                   if (abs(emb-n)/n)*100<5:
                       iteration=counter
                       break
               iteration_relError5_ffurer.append(iteration)
                       
               avg_embeddings_ffurer.append(np.mean(np.array(all_embeddings)))
               final_emb=0
               if not row[final_embedding_index]=='':
                   embeddings_ffurer.append(float(row[final_embedding_index])) #QUESTION: take average or final?
                   if (row[final_std_index]):
                       std_embeddings_ffurer.append(float(row[final_std_index]))
                   else:
                       std_embeddings_ffurer.append(row[final_std_index])
               else:
                   embeddings_ffurer.append(0) #QUESTION: take average or final?
                   std_embeddings_ffurer.append(0)
            for c, col in enumerate(row):
                if(not c in false_furer_max_column_width.keys()):
                    false_furer_max_column_width[c]=0
                if(len(col)>false_furer_max_column_width[c]):
                    false_furer_max_column_width[c]=len(col)
                try:
                    if float(col):
                         worksheet2.write_number(r, c, col)
                    else:    
                         worksheet2.write(r, c, col)
                except:
                    worksheet2.write(r, c, col)
            col=1
            for e in relErrorEmbeddings:
                worksheet1_relError.write(r,col,e)
                col+=1
    for c in false_furer_max_column_width.keys():
        worksheet2.set_column(c,c, false_furer_max_column_width[c]+2)
    worksheet2.set_column(1,1, 20)
    worksheet1_relError.set_column(1,1, 20)
    
    
    #CSV furer-AD-ord
    worksheet2 = workbook.add_worksheet("furer_AD_ord")
    worksheet1_relError = workbook.add_worksheet("furer_AD_RelError_ord")
    with open(os.path.join(csv_path,'Ffurer_order_random_'+str(level)+'.csv'), 'rb') as f:
        reader = csv.reader(f)
        initial_embedding_index=-1
        final_embedding_index=-1
        final_std_index=-1
        index_range_all_embeddings=[]
        for r, row in enumerate(reader):
            relErrorEmbeddings=[]
            if r==0:
                initial_embedding_index=row.index("emb_1")
                final_embedding_index=row.index("emb_120")
                final_std_index=row.index("std_120")
                index_range_all_embeddings=range(initial_embedding_index,final_embedding_index+1)
                worksheet1_relError.write(0,0,row[0])
                for i in range(1,120):
                    worksheet1_relError.write(0,i,'emb_'+str(i))
            if r>0:
               all_embeddings=[]
               for i in np.array(row)[np.array(index_range_all_embeddings)]:
                   if not i=='':
                      all_embeddings.append(float(i))
                   else:
                      all_embeddings.append(0)
               counter=0
               for emb in all_embeddings:
                   n=None
                   if embeddings_exhaustive[r-1]==0:
                       n=1
                   else:
                       n=embeddings_exhaustive[r-1]
                   if n!=None and emb!=None:
                      relErrorEmbeddings.append(abs(emb-n)/n)
                   else:
                       relErrorEmbeddings.append(None)
               iteration=len(all_embeddings)
               for emb in all_embeddings:
                   counter+=1
                   if emb==None or n==None:
                       iteration=None
                       break
                   if (abs(emb-n)/n)*100<5:
                       iteration=counter
                       break
               iteration_relError5_ffurer.append(iteration)
                       
               avg_embeddings_ffurer.append(np.mean(np.array(all_embeddings)))
               final_emb=0
               if not row[final_embedding_index]=='':
                   embeddings_ffurer.append(float(row[final_embedding_index])) #QUESTION: take average or final?
                   if (row[final_std_index]):
                       std_embeddings_ffurer.append(float(row[final_std_index]))
                   else:
                       std_embeddings_ffurer.append(row[final_std_index])
               else:
                   embeddings_ffurer.append(0) #QUESTION: take average or final?
                   std_embeddings_ffurer.append(0)
            for c, col in enumerate(row):
                if(not c in false_furer_max_column_width.keys()):
                    false_furer_max_column_width[c]=0
                if(len(col)>false_furer_max_column_width[c]):
                    false_furer_max_column_width[c]=len(col)
                try:
                    if float(col):
                         worksheet2.write_number(r, c, col)
                    else:    
                         worksheet2.write(r, c, col)
                except:
                    worksheet2.write(r, c, col)
            col=1
            for e in relErrorEmbeddings:
                worksheet1_relError.write(r,col,e)
                col+=1
    for c in false_furer_max_column_width.keys():
        worksheet2.set_column(c,c, false_furer_max_column_width[c]+2)
    worksheet2.set_column(1,1, 20)
    worksheet1_relError.set_column(1,1, 20)
       
    #CSV random
    worksheet3 = workbook.add_worksheet("random")
    worksheet1_relError = workbook.add_worksheet("random_RelError")
    with open(os.path.join(csv_path,'random_'+str(level)+'.csv'), 'rb') as f:
        reader = csv.reader(f)
        final_embedding_index=-1
        final_std_index=-1
        initial_embedding_index=-1
        index_range_all_embeddings=[]
        for r, row in enumerate(reader):
            relErrorEmbeddings=[]
            if r==0:
                initial_embedding_index=row.index("emb_1")
                final_embedding_index=row.index("emb_120")
                final_std_index=row.index("std_120")
                index_range_all_embeddings=range(initial_embedding_index,final_embedding_index+1)
                worksheet1_relError.write(0,0,row[0])
                for i in range(1,120):
                    worksheet1_relError.write(0,i,'emb_'+str(i))
            if r>0:
               all_embeddings=[]
               for i in np.array(row)[np.array(index_range_all_embeddings)]:
                   if not i=='':
                      all_embeddings.append(float(i))
                   else:
                      all_embeddings.append(0)
               counter=0
               for emb in all_embeddings:
                   n=None
                   if embeddings_exhaustive[r-1]==0:
                       n=1
                   else:
                       n=embeddings_exhaustive[r-1]
                   if n!=None and emb!=None:
                      relErrorEmbeddings.append(abs(emb-n)/n)
                   else:
                       relErrorEmbeddings.append(None)
               iteration=len(all_embeddings)
               for emb in all_embeddings:
                   counter+=1
                   if emb==None or n==None:
                       iteration=None
                       break
                   if (abs(emb-n)/n)*100<5:
                       iteration=counter
                       break
               iteration_relError5_random.append(iteration)
               avg_embeddings_random.append(np.mean(np.array(all_embeddings)))
               if not row[final_embedding_index]=='':
                   embeddings_random.append(float(row[final_embedding_index])) #QUESTION: take average or final?
                   std_embeddings_random.append(float(row[final_std_index]))
               else:
                   embeddings_random.append(0) #QUESTION: take average or final?
                   std_embeddings_random.append(0)
            for c, col in enumerate(row):
                if(not c in random_max_column_width.keys()):
                    random_max_column_width[c]=0
                if(len(col)>random_max_column_width[c]):
                    random_max_column_width[c]=len(col)
                try:
                    if float(col):
                         worksheet3.write_number(r, c, col)
                    else:    
                         worksheet3.write(r, c, col)
                except:
                    worksheet3.write(r, c, col)
            col=1
            for e in relErrorEmbeddings:
                worksheet1_relError.write(r,col,e)
                col+=1
    for c in random_max_column_width.keys():
        worksheet3.set_column(c,c, random_max_column_width[c]+2)
    worksheet3.set_column(1,1, 20)
    worksheet1_relError.set_column(1,1, 20)
    
    #WRITING RELATIVE ERRORS OF FINAL EMBEDDINGS
    worksheet4 = workbook.add_worksheet("relErrorEmbedding")
    worksheet4.write(0,0,'pattern')
    worksheet4.write(0,1,'relEFurer-OBD')
    worksheet4.write(0,2,'relEFurer-AD')
    worksheet4.write(0,3,'relError-Rnd')
    
    
    for i in range(0,len(embeddings_exhaustive)):
            absError_furer=None
            absError_ffurer=None
            absError_random=None
            if embeddings_exhaustive[i]==0:
                embeddings_exhaustive[i]=1
                embeddings_furer[i]+=1
                embeddings_ffurer[i]+=1
                embeddings_random[i]+=1
            try:
              absError_furer=abs(embeddings_furer[i]-embeddings_exhaustive[i])/float(embeddings_exhaustive[i])
            except:
                absError_furer=None
            try:
              absError_ffurer=abs(embeddings_ffurer[i]-embeddings_exhaustive[i])/float(embeddings_exhaustive[i])
            except:
                absError_ffurer=None
            try:
              absError_random=abs(embeddings_random[i]-embeddings_exhaustive[i])/float(embeddings_exhaustive[i])
            except:
                absError_random=None
            
            worksheet4.write(i+1,0,pattern_ids[i])
            worksheet4.write(i+1,1,absError_furer)
            worksheet4.write(i+1,2,absError_ffurer)
            worksheet4.write(i+1,3,absError_random)
           
            
            
    worksheet4.set_column(1,1, 20)
    worksheet4.set_column(1,2, 20)
    worksheet4.set_column(1,3, 20)
    worksheet4.set_column(1,4, 20)
    
    #WRITING RELATIVE ERRORS OF AVERAGE EMBEDDINGS
    worksheet4 = workbook.add_worksheet("relErrorAvgEmbedding")
    worksheet4.write(0,0,'pattern')
    worksheet4.write(0,1,'relEFurer-OBD')
    worksheet4.write(0,2,'relEFurer-AD')
    worksheet4.write(0,3,'relError-Rnd')
    for i in range(0,len(embeddings_exhaustive)):
            absError_furer=None
            absError_ffurer=None
            absError_random=None
             
            try:
              absError_furer=abs(avg_embeddings_furer[i]-embeddings_exhaustive[i])/float(embeddings_exhaustive[i])
            except:
                absError_furer=None
            try:    
              absError_ffurer=abs(avg_embeddings_ffurer[i]-embeddings_exhaustive[i])/float(embeddings_exhaustive[i])
            except:
                absError_ffurer=None
            try:    
              absError_random=abs(avg_embeddings_random[i]-embeddings_exhaustive[i])/float(embeddings_exhaustive[i])
            except:
                absError_random=None
            worksheet4.write(i+1,0,pattern_ids[i])
            worksheet4.write(i+1,1,absError_furer)
            worksheet4.write(i+1,2,absError_ffurer)
            worksheet4.write(i+1,3,absError_random)
    worksheet4.set_column(1,1, 20)
    worksheet4.set_column(1,2, 20)
    worksheet4.set_column(1,3, 20)
    worksheet4.set_column(1,4, 20)
    
    
    #WRITING Iteration number at which relative error < 5 %
    worksheet4 = workbook.add_worksheet("iterationRelError<5")
    worksheet4.write(0,0,'pattern')
    worksheet4.write(0,1,'#emb_exh')
    worksheet4.write(0,2,'Iteration_Furer-OBD')
    worksheet4.write(0,3,'Iteration_Furer-AD')
    worksheet4.write(0,4,'Iteration_Rnd')
    for i in range(0,len(embeddings_exhaustive)):
            worksheet4.write(i+1,0,pattern_ids[i])
            worksheet4.write(i+1,1,embeddings_exhaustive[i])
            try:
             worksheet4.write(i+1,2,iteration_relError5_furer[i])
            except:
             worksheet4.write(i+1,2,None)
            try:   
             worksheet4.write(i+1,3,iteration_relError5_ffurer[i])
            except:
             worksheet4.write(i+1,3,None)
            try:
             worksheet4.write(i+1,4,iteration_relError5_random[i])
            except:
             worksheet4.write(i+1,4,None)
    worksheet4.set_column(1,1, 20)
    worksheet4.set_column(1,2, 20)
    worksheet4.set_column(1,3, 20)
    worksheet4.set_column(1,4, 20)        
    workbook.close()
"""
