graph [
  name "/data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/PATTERNS/PATTERNS_DBLP/PATTERNS_400_BATCH/patterns_size_6/batch1/dblppattern_e8f8dbe695f84843bf60b78a33ea06bc/dblppattern_e8f8dbe695f84843bf60b78a33ea06bc.gml"
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
    label "citations = low"
    predicate "citations"
    target 0
    valueinpattern 1
    type "None"
    value "low"
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
]
