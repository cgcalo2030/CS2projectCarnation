[v2.0.0] - 2026-2-15
●Added / Improved
-Improved input validation to prevent user errors
-Refactored functions for better readability
-Cleaner progress summary display
-More organized data handling and menu flow

●Retained Features
-Add, edit, and delete subjects
-Log weekly study hours
-Automatic weekly reset of progress
-Local data storage using JSON
●Not Included
-Online accounts or cloud syncing
-Graphical user interface
●Technologies Used
-Python (core language)
-JSON (local data storage)
-GitHub (version control)

References (APA)
Association for Computing Machinery. (2018). ACM Code of Ethics and Professional Conduct. https://www.acm.org/code-of-ethics�

---------------3RD QUARTER--------------

[v1.2.0] - 2025-12-05
​Added (New Features)
​Progress Visualizer: Introduced a console-based progress bar ([======-----]) for each subject, providing an instant visual status of goal completion.
​Goal Completion Notifications: Added a system that displays a celebratory notification when a subject's weekly study goal hits 100% or more.
​Persistence Check: Added logic to automatically check for and load study_data.json upon startup.
​Improved (Enhancements)
​Data Structure Upgrade: Refactored internal data structure to better handle cumulative hours and reset weekly goals automatically on Monday (simulated reset for demo purposes).
​User Experience: Enhanced menu prompts and display tables for better readability and alignment.


​[v1.1.0] - 2025-11-28
​Added (New Features)
​Edit/Delete Subjects: Implemented functionality to allow users to modify the name or delete an existing subject entirely.
​Set/Modify Goals: Users can now set or update the weekly goal (in hours) for any existing subject.
​Error Handling: Added robust input validation to prevent crashes from non-numeric or invalid menu selections.
​Improved (Enhancements)
​Summary Table: Improved the main summary display to show "Goal (Hours)" and "Studied (Hours)" side-by-side for easier comparison.
​Saving Logic: Enhanced JSON serialization/deserialization to ensure cleaner data files.


​[v1.0.0] - 2025-11-20
​Added (Initial Features)
​Core Subject Management: Functionality to add new subjects to the study list.
​Initial Goal Setting: Basic command to set a weekly study time goal for a subject.
​Time Logging: Core logic to record study time updates for a subject.
​Progress Calculation: Basic function to calculate and display the percentage of the goal completed.
​Data Persistence: Implemented saving and loading of study data using study_data.json.
​Menu System: Simple, menu-driven command-line interface for navigation.


