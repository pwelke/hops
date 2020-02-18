graph [
  name "invalid"
  node [
    id 0
    label "phenotype"
    predicate "phenotype"
    target 1
    valueinpattern 0
    type "None"
  ]
  node [
    id 1
    label "constant:protein"
    predicate "constant"
    target 0
    valueinpattern 0
    type "None"
  ]
  node [
    id 2
    label "interaction"
    predicate "interaction"
    target 0
    valueinpattern 0
    type "None"
  ]
  node [
    id 3
    label "phenotype = Phenotype_id_52030005010"
    predicate "phenotype"
    target 0
    valueinpattern 1
    type "None"
    value "Phenotype_id_52030005010"
  ]
  edge [
    source 0
    target 1
  ]
  edge [
    source 1
    target 2
  ]
  edge [
    source 1
    target 3
  ]
]
