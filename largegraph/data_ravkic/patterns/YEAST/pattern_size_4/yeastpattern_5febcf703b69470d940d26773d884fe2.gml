graph [
  name "invalid"
  node [
    id 0
    label "interaction"
    predicate "interaction"
    target 0
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
    label "function"
    predicate "function"
    target 1
    valueinpattern 0
    type "None"
  ]
  node [
    id 3
    label "protein_class = Pc_id_181011011"
    predicate "protein_class"
    target 0
    valueinpattern 1
    type "None"
    value "Pc_id_181011011"
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
