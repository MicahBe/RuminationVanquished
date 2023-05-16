document.addEventListener('DOMContentLoaded', function () {
    const addThoughtBtn = document.getElementById('addThoughtBtn');
    const thoughtsContainer = document.getElementById('thoughtsContainer');

    addThoughtBtn.addEventListener('click', addThought);

    function addThought() {
        const thoughtText = prompt('Enter your thought:');
        if (!thoughtText) return;

        fetch('/thoughts', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ content: thoughtText })
        })
        .then(response => response.json())
        .then(thought => {
            const thoughtDiv = createThought(thought);
            thoughtsContainer.appendChild(thoughtDiv);
        });
    }

    function createThought(thought) {
        const thoughtDiv = document.createElement('div');
        thoughtDiv.classList.add('thought');
        thoughtDiv.textContent = thought.content;
        thoughtDiv.addEventListener('click', () => {
            fetch('/alternatives', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ thought_id: thought.id })
            })
            .then(response => response.json())
            .then(alternative => {
                // Display existing selected alternative if available
            const existingSelectedAlternative = thought.alternatives.find(a => a.selected);
            const initialAlternativeText = existingSelectedAlternative ? existingSelectedAlternative.content : alternative.content;
            
            const alternativeText = prompt('Alternative thought:', initialAlternativeText);
            if (!alternativeText) return;

            if (alternativeText === alternative.content || (existingSelectedAlternative && alternativeText === existingSelectedAlternative.content)) {
                // Save the alternative as selected
                const altId = existingSelectedAlternative ? existingSelectedAlternative.id : alternative.id;
                fetch(`/alternatives/${altId}/select`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => response.json())
                .then(result => {
                    if (result.success) {
                        console.log('Alternative selected');
                    } else {
                        console.error('Failed to select alternative');
                    }
                });
            } else {
                // Save a new alternative as selected
                fetch(`/alternatives/${alternative.id}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ content: alternativeText })
                })
                .then(response => response.json())
                .then(result => {
                    if (result.success) {
                        console.log('Alternative updated and selected');
                    } else {
                        console.error('Failed to update and select alternative');
                    }
                });
            }
            });
        });
        
    return thoughtDiv;
    }

    function addThoughtToPage(content, id) {
        let thoughtElement = document.createElement('div');
        thoughtElement.textContent = content;
        thoughtElement.id = id;
        document.body.appendChild(thoughtElement);
    }


    // initial placement of "return thoughtDiv;"


// Load existing thoughts
fetch('/thoughts')
    .then(response => response.json())
    .then(thoughts => {
        for (let thought of thoughts) {
            addThoughtToPage(thought.content, thought.id);
        }
    })
    .catch(error => console.error('Error:', error));

});