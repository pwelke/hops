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
    label "constant:paper"
    predicate "constant"
    target 0
    valueinpattern 0
    type "None"
  ]
  node [
    id 4
    label "references"
    predicate "references"
    target 0
    valueinpattern 0
    type "None"
  ]
  node [
    id 5
    label "references"
    predicate "references"
    target 0
    valueinpattern 0
    type "None"
  ]
  node [
    id 6
    label "dir"
    predicate "dir"
    target 0
    valueinpattern 0
    type "None"
  ]
  node [
    id 7
    label "dir"
    predicate "dir"
    target 0
    valueinpattern 0
    type "None"
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
    target 5
  ]
  edge [
    source 2
    target 3
  ]
  edge [
    source 3
    target 4
  ]
  edge [
    source 3
    target 6
  ]
  edge [
    source 3
    target 7
  ]
  edge [
    source 5
    target 7
  ]
]
