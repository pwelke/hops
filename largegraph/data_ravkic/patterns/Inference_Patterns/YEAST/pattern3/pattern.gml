graph [
name "pattern2"
  node [
    id 1
    label "constant:protein"
    predicate "constant"
    target 1
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
    label "function"
    predicate "function"
    target 1
    valueinpattern 0
    type "None"
  ]
  node [
    id 4
    label "interaction"
    predicate "interaction"
    target 1
    valueinpattern 0
    value "True"
    type "None"
  ]
  node [
    id 5
    label "constant:protein"
    predicate "constant"
    target 1
    valueinpattern 0
    type "None"
    binds 1
  ]
  node [
    id 6
    label "location"
    predicate "location"
    target 1
    valueinpattern 0
    type "None"
  ]
    edge [
    source 1
    target 4
  ]
   edge [
    source 1
    target 6
  ]
      edge [
    source 1
    target 2
  ]
  edge [
    source 4
    target 5
  ]
    edge [
    source 5
    target 3
  ]
]

