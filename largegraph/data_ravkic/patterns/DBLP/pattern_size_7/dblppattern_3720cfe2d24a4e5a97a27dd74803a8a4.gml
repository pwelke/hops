graph [
  name "invalid"
  node [
    id 0
    label "citations"
    predicate "citations"
    target 1
    valueinpattern 0
    type "None"
  ]
  node [
    id 1
    label "constant:paper"
    predicate "constant"
    target 0
    valueinpattern 0
    type "None"
  ]
  node [
    id 2
    label "coauthored"
    predicate "coauthored"
    target 0
    valueinpattern 0
    type "None"
  ]
  node [
    id 3
    label "references"
    predicate "references"
    target 0
    valueinpattern 0
    type "None"
  ]
  node [
    id 4
    label "constant:paper"
    predicate "constant"
    target 0
    valueinpattern 0
    type "None"
  ]
  node [
    id 5
    label "dir"
    predicate "dir"
    target 0
    valueinpattern 0
    type "None"
  ]
  node [
    id 6
    label "citations = high"
    predicate "citations"
    target 0
    valueinpattern 1
    type "None"
    value "high"
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
  edge [
    source 2
    target 4
  ]
  edge [
    source 4
    target 5
  ]
  edge [
    source 4
    target 6
  ]
]
