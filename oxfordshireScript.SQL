select top 5 
lp.UPN, 
upn.FormerUPN,
eth.ethnicitySource, 
eth.ethnicityCode,
lp.InCare_LAId,
lse.ExitDate,
lsn.MedicalFlag,
lp.ModeOfTravel,
lse.MembershipType,
lsn.SpecialisedResourcesLevel,
lsn.StartDate,
lsn.EndDate,
lsn.Provision,
lp.Traveller_Code,
*
from LearnerPersonal lp 
left join FormerUPN upn on lp.RefId = upn.OwnerRefId
left join Ethnicity eth on lp.RefId = eth.OwnerRefId
left join Language lan on lp.RefId = lan.OwnerRefId
left join LearnerEntitlement fsm on lp.RefId = fsm.LearnerPersonalRefId
left join LearnerSchoolEnrolment lse on lp.RefId = lse.RefId
left join LearnerSpecialNeeds lsn on lp.RefId = lsn.RefId
join SIF_ExtendedElement see on lp.ZoneId = see.zoneId and see.OwnerType = 'schoolinfo' and see.SIF_Value = 'SIMSnet'
-- where upn.FormerUPN is not null
-- where eth.ethnicitySource is not null 
-- where eth.ethnicityCode is not null
-- where lp.InCare_LAId is not null
-- where lp.InCare_Current is not null
-- where lse.EntryDate is not null
-- where lse.ExitDate is not null
-- where lp.ModeOfTravel is not null
-- where lse.MembershipType is not null
-- where lsn.StartDate is not null
-- where lsn.EndDate is not null
-- where lsn.Provision is not null
-- where lp.Traveller_Code is not null


/**
List of MIS
g2
Bromcom
SIMSnet
scholarpack
Schoolpod
**/
;

-- Queue Enrty Query, can be used to view requests and object count, add the DFE code to the ZoneID

SELECT * 
FROM QueueEntry
WHERE zoneid = ''
AND SIFObject = 'LearnerPersonal'
-- AND context = 'SIF_Default'
AND addedToQueueDateTime > '2024-09-01' --After date
AND addedToQueueDateTime < '2025-02-12' --Before date
ORDER BY addedToQueueDateTime DESC;
