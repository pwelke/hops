graph [
  node [
    id 0
    label "ref"
    predicate "ref"
    target 0
    valueinpattern 0
    type "None"
  ]
  node [
    id 1
    label "page = department"
    predicate "page"
    target 0
    valueinpattern 1
    type "None"
    value "department"
  ]
  node [
    id 2
    label "page"
    predicate "page"
    target 1
    valueinpattern 0
    type "None"
  ]
  node [
    id 3
    label "dir"
    predicate "dir"
    target 0
    valueinpattern 0
    type "None"
  ]
  edge [
    source 0
    target 2
  ]
  edge [
    source 0
    target 3
  ]
  edge [
    source 1
    target 3
  ]
]
