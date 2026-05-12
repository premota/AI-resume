# Job parser

Planned layout for a job-description parsing stack: an installable parsing framework plus a thin HTTP service.

## Layout

```


JD_parser/  
    │          # FRAMEWORK (installable package)
    ├── core/
│   │   ├── pipeline.py
│   │   ├── parser.py
│   │
│   ├── extractors/
│   │   ├── base.py
│   │   ├── regex.py
│   │   ├── llm.py
│   │
│   ├── schemas/
│   │   └── job.py
│   │
│   ├── config/
│   │   └── jd_config.py  # contains the config needed to handle JD text
│   │
│   └── __init__.py
|

