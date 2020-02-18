graph [
name "pattern1"
  node [
    id 1
    label "constant"
    predicate "constant"
    target 0
    valueinpattern 0
    type "None"
  ]
  node [
    id 2
    label "constant"
    predicate "constant"
    target 0
    valueinpattern 0
    type "None"
  ]
  node [
    id 3
    label "constant"
    predicate "constant"
    target 0
    valueinpattern 0
    type "None"
  ]
  node [
    id 4
    label "interaction"
    predicate "interaction"
    target 0
    valueinpattern 0
    type "None"
  ]
  node [
    id 5
    label "interaction"
    predicate "interaction"
    target 0
    valueinpattern 0
    type "None"
  ]
  node [
    id 6
    label "function"
    predicate "function"
    target 1
    valueinpattern 0
    type "None"
  ]
  node [
    id 7
    label "function"
    predicate "function"
    target 1
    valueinpattern 0
    type "None"
  ]
  node [
    id 8
    label "location"
    predicate "location"
    target 1
    valueinpattern 0
    type "None"
  ] 
  edge [
    source 1
    target 8
  ]
   edge [
    source 1
    target 4
  ]
      edge [
    source 4
    target 2
  ]
  edge [
    source 2
    target 5
  ]
    edge [
    source 5
    target 3
  ]
   edge [
    source 6
    target 3
  ]
  edge [
    source 7
    target 1
  ]
]

