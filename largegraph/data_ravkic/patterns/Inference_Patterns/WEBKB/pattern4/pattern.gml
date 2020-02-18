graph [
name "pattern4"
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
    label "page"
    predicate "page"
    target 1
    valueinpattern 0
    type "None"
  ]
  node [
    id 4
    label "page_class"
    predicate "page_class"
    target 1
    valueinpattern 0
    type "None"
  ]
  node [
    id 5
    label "word"
    predicate "word"
    target 1
    valueinpattern 0
    type "None"
  ]
    node [
    id 6
    label "linked"
    predicate "linked"
    target 1
    valueinpattern 0
    type "None"
  ]
   node [
    id 7
    label "linked"
    predicate "linked"
    target 1
    valueinpattern 0
    type "None"
  ]
    node [
    id 8
    label "word"
    predicate "word"
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
    target 5
  ]
   edge [
    source 1
    target 6
  ]
   edge [
    source 6
    target 2
  ]
   edge [
    source 2
    target 7
  ]
   edge [
    source 7
    target 3
  ]
   edge [
    source 3
    target 8
  ]
]

