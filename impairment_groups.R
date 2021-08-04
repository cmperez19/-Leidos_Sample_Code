#calculated the number impairments for each patient 
#determined if patient had an impairment represented as a boolean  
load("NOVI_24mo_outcome.RData")
load("bmiqSet.Rdata")

commonSamples = as.character(intersect(colnames(bmiqSet), novi.24mo_outcome$id))
rownames(novi.24mo_outcome) = as.character(novi.24mo_outcome$id)
novi.24mo_outcome = novi.24mo_outcome[commonSamples,] #568 -> 451
bmiqSet = bmiqSet[,commonSamples] 

novi.24mo_outcome$mchatfc3_bin = novi.24mo_outcome$mchatfc3 == "High Risk (10 or above)"
novi.24mo_outcome$mchatfc3_bin = as.numeric(novi.24mo_outcome$mchatfc3_bin) 
novi.24mo_outcome$mh24cpsev_bin = novi.24mo_outcome$mh24cpsev == "3) Severe (GMFCS Level 4-5)"
novi.24mo_outcome$mh24cpsev_bin = as.numeric(novi.24mo_outcome$mh24cpsev_bin)
novi.24mo_outcome$extc_bin = novi.24mo_outcome$extc == "T>=64"
novi.24mo_outcome$intc_bin = novi.24mo_outcome$intc == "T>=64"
novi.24mo_outcome$baycCOGlo2_bin = novi.24mo_outcome$baycCOGlo2 == "Composite < 70"
novi.24mo_outcome$baycLANGlo2_bin = novi.24mo_outcome$baycLANGlo2 == "Composite < 70"
novi.24mo_outcome$baycMOTlo2_bin = novi.24mo_outcome$baycMOTlo2 == "Composite < 70"
outcomes = c("mchatfc3_bin", "mh24cpsev_bin", "extc_bin", "intc_bin", 
             "baycCOGlo2_bin", "baycLANGlo2_bin", "baycMOTlo2_bin")

novi.24mo_outcome$any_impairment = NA 
novi.24mo_outcome$total_impariment = 0

#if statement == T or each then the row for novi.24mo_outcomes$combined will turn T 

for (i in 1:451){
novi.24mo_outcome$any_impairment[i] = 1 %in% novi.24mo_outcome[i, outcomes] | TRUE %in% novi.24mo_outcome[i,outcomes] == T
print(novi.24mo_outcome$any_impairment[i]) 
if(novi.24mo_outcome$any_impairment[i] == T){
  total_impairments = c()
  total_impairments[1] = novi.24mo_outcome[i, outcomes[1]] == 1 
  total_impairments[2] = novi.24mo_outcome[i, outcomes[2]] == 1
  total_impairments[3] = novi.24mo_outcome[i, outcomes[3]] == T 
  total_impairments[4] = novi.24mo_outcome[i, outcomes[4]] == T 
  total_impairments[5] = novi.24mo_outcome[i, outcomes[5]] == T 
  total_impairments[6] = novi.24mo_outcome[i, outcomes[6]] == T
  total_impairments[7] = novi.24mo_outcome[i, outcomes[7]] == T
  total_impairments = total_impairments[!is.na(total_impairments)]
  novi.24mo_outcome$total_impariment[i] = sum(total_impairments)
  
  print(novi.24mo_outcome$total_impariment[i])
}
}

barplot(table(novi.24mo_outcome$total_impariment),main="Distribution of Total Impairments",
        xlab="Number of Impairments",
        ylab="Count" )

counts_by_impairment = matrix(NA, nrow = 1, ncol = 7)
counts_by_impairment[1,1] =sum(novi.24mo_outcome$mchatfc3_bin[!is.na(novi.24mo_outcome$mchatfc3_bin)])
counts_by_impairment[1,2] = sum(novi.24mo_outcome$mh24cpsev_bin[!is.na(novi.24mo_outcome$mh24cpsev_bin)]) 
counts_by_impairment[1,3] = sum(novi.24mo_outcome$extc_bin[!is.na(novi.24mo_outcome$extc_bin)]) 
counts_by_impairment[1,4] = sum(novi.24mo_outcome$intc_bin[!is.na(novi.24mo_outcome$intc_bin)]) 
counts_by_impairment[1,5]= sum(novi.24mo_outcome$baycCOGlo2_bin[!is.na(novi.24mo_outcome$baycCOGlo2_bin)]) 
counts_by_impairment[1,6] = sum(novi.24mo_outcome$baycLANGlo2_bin[!is.na(novi.24mo_outcome$baycLANGlo2_bin)]) 
counts_by_impairment[1,7] = sum(novi.24mo_outcome$baycMOTlo2_bin[!is.na(novi.24mo_outcome$baycMOTlo2_bin)])


colnames(counts_by_impairment) = c("mchatfc3", "mh24cpsev", "extc", "intc", 
                                   "baycCOGlo2", "baycLANGlo2", "baycMOTlo2")
barplot(counts_by_impairment, xlab = "Impairment Variable Name", ylab = "Count", main = "Impairment Counts")
