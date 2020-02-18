graph [
  name "invalid"
  node [
    id 0
    label "0"
    predicate "interaction"
    target 0
    valueinpattern 0
    type "None"
  ]
  node [
    id 1
    label "1"
    predicate "constant"
    target 0
    valueinpattern 0
    type "None"
  ]
  node [
    id 2
    label "2"
    predicate "protein_class"
    target 1
    valueinpattern 0
    type "None"
  ]
  node [
    id 3
    label "3"
    predicate "function"
    target 0
    valueinpattern 1
    type "None"
    value "Func_id_1"
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
