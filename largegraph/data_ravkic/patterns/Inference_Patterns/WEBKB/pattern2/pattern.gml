graph [
name "pattern2"
  node [
    id 1
    label "page"
    predicate "page"
    target 1
    valueinpattern 0
    type "None"
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
    label "page_class"
    predicate "page_class"
    target 1
    valueinpattern 0
    type "None"
  ]
  node [
    id 4
    label "word"
    predicate "word"
    target 1
    valueinpattern 0
    type "None"
  ]
    node [
    id 5
    label "linked"
    predicate "linked"
    target 1
    valueinpattern 0
    type "None"
  ]
    node [
    id 6
    label "word"
    predicate "word"
    target 1
    valueinpattern 0
    type "None"
  ]
   edge [
    source 1
    target 3
  ]
  edge [
    source 1
    target 4
  ]
   edge [
    source 1
    target 5
  ]
   edge [
    source 5
    target 2
  ]
   edge [
    source 2
    target 6
  ]
]

