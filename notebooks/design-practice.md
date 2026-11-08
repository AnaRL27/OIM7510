# TV Show Database — Entity Relationship Diagram

```mermaid
erDiagram
    TV_SERIES ||--o{ RATINGS : has
    TV_SERIES ||--o{ GENRE : has
    TV_SERIES ||--o{ WRITERS : has
    TV_SERIES ||--o{ STARS : has

    TV_SERIES {
        int    id PK
        string title
        int    year
        int    episode
    }
    RATINGS {
        int   show_id PK, FK
        float rating
        int   votes
    }
    GENRE {
        int show_id PK, FK
        int genre_id PK, FK
    }
    WRITERS {
        int show_id PK, FK
        int person_id PK, FK
    }
    STARS {
        int show_id PK, FK
        int person_id PK, FK
    }
```
