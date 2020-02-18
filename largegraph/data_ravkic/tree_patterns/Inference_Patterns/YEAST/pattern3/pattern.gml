graph [
  name "pattern2"
  node [
    id 0
    label "1"
    predicate "constant"
    target 1
    valueinpattern 0
    type "None"
  ]
  node [
    id 1
    label "2"
    predicate "function"
    target 1
    valueinpattern 0
    type "None"
  ]
  node [
    id 2
    label "3"
    predicate "function"
    target 1
    valueinpattern 0
    type "None"
  ]
  node [
    id 3
    label "4"
    predicate "interaction"
    target 1
    valueinpattern 0
    value "True"
    type "None"
  ]
  node [
    id 4
    label "5"
    predicate "constant"
    target 1
    valueinpattern 0
    type "None"
    binds 1
  ]
  node [
    id 5
    label "6"
    predicate "location"
    target 1
    valueinpattern 0
    type "None"
  ]
  edge [
    source 0
    target 3
  ]
  edge [
    source 0
    target 5
  ]
  edge [
    source 0
    target 1
  ]
  edge [
    source 2
    target 4
  ]
  edge [
    source 3
    target 4
  ]
]
