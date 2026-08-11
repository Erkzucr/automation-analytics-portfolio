# Dashboard Specification

## Page 1: Executive Overview
- Cards: Total Case Studies, Executable Demos, Total Documented Tests, Advanced Case Studies
- Horizontal bar chart: capability by demonstration depth
- Donut chart: case studies by complexity
- Slicer: capability
- Text callout: Synthetic data only

## Page 2: Case Study Explorer
- Matrix: case ID, capability, complexity, depth, tests, status
- Conditional formatting on demonstration depth
- Slicers: complexity, capability, status
- Tooltip: data classification

## Page 3: Executable Demo Results
- Clustered column chart: accepted vs exception count by technology
- Cards: Total Accepted Records, Total Exception Records, Exception Rate
- Table: demo name, technology, test status, data classification
- Slicer: technology

## Design
- Navy: #163A5F
- Blue: #1F4E78
- Light blue: #EAF1F7
- Green: #2E7D32
- Orange: #C65911
- Use a 16:9 canvas and keep all page backgrounds white.
