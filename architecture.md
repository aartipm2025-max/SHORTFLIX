# ShortFlix Architecture and Project Plan

## Overview
ShortFlix is a streamlined, fast-loading discovery platform for short films. The primary goal is to minimize decision fatigue by allowing users to select a genre and immediately start watching curated short films.

## Tech Stack
- **Frontend / Deployment:** Streamlit (Python)
- **Data storage:** Static JSON or Python Dictionary (No complex backend DB to ensure fast loading and simplicity)
- **UI/UX:** Minimalist light theme, utilizing Streamlit's layout containers and markdown with custom CSS for a card-based aesthetic.

## System Architecture

The application will be structured into modular components:

1.  **State Management:** Session state will be extensively used to manage navigation between the "Home", "Recommendations", and "Video Player" views without full page reloads.
2.  **Data Layer:** A predefined catalog of short films (50-100 entries).
3.  **UI Layer:**
    -   **Home View:** Renders massive genre cards.
    -   **Recommendations View:** Applies filters, randomly selects 5 films, and renders them in a styled card layout.
    -   **Video View:** Displays the embedded YouTube player inside Streamlit, along with metadata and navigation controls.

## Application Flow (State Machine)
- `state.page` = "HOME" | "RECOMMENDATIONS" | "VIDEO"
- `state.selected_genre` = None | string
- `state.current_video` = None | dict
- `state.current_recommendations` = list

## Phased Implementation Plan

### Phase 1: Foundation & Architecture
- [x] Define application architecture and user flows.
- [ ] Initialize Streamlit project structure.

### Phase 2: Data Preparation
- [ ] Create `data.py` to act as our local database.
- [ ] Populate it with an initial set of sample YouTube short films categorized by genre (Sci-Fi, Romantic, Intense, Comedy, Casual) and duration.

### Phase 3: Core UI Framework & State Management
- [ ] Set up `app.py`.
- [ ] Implement Streamlit session state initialization to handle routing between Home, Recommendations, and Video pages.

### Phase 4: Page Implementations
- [ ] **Home Page:** Implement the "What do you feel like watching?" prompt and clickable genre cards.
- [ ] **Recommendations Page:** Implement the filtering logic (duration filter), random selection of 5 films, layout components (thumbnails, metadata), and the "Show another 5" feature.
- [ ] **Video Player Page:** Implement YouTube embed, display metadata, "Next Film" button, and "Back to list" navigation.

### Phase 5: Styling & Polish
- [ ] Inject custom CSS to make Streamlit look more like a modern, minimalist web app.
- [ ] Ensure light theme is enforced.
- [ ] Test end-to-end functionality.
