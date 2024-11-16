document.getElementById("schedule-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    // Collect user input
    const formData = {
        interests: document.getElementById("interests").value,
        credits_per_semester: parseInt(document.getElementById("credits").value),
        transfer_credits: parseInt(document.getElementById("transfer_credits").value),
        completed_courses: document.getElementById("completed_courses").value.split(',').map(course => course.trim())
    };

    // Send data to the backend
    try {
        const response = await fetch("/generate_schedule", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(formData)
        });

        // Parse the response
        if (!response.ok) throw new Error("Failed to generate schedule");
        const schedule = await response.json();

        // Display the schedule
        const outputDiv = document.getElementById("schedule-output");
        outputDiv.innerHTML = "<h2>Proposed Schedule</h2>";

        if (schedule.length === 0) {
            outputDiv.innerHTML += "<p>No schedule could be generated. Please check your input and try again.</p>";
        } else {
            schedule.forEach(semester => {
                const semesterDiv = document.createElement("div");
                semesterDiv.innerHTML = `
                    <h3>Semester ${semester.Semester}</h3>
                    <p><strong>Courses:</strong> ${semester.Courses.join(", ")}</p>
                    <p><strong>Credits:</strong> ${semester.Credits}</p>`;
                outputDiv.appendChild(semesterDiv);
            });
        }
    } catch (error) {
        console.error("Error:", error);
        alert("An error occurred while generating the schedule. Please try again.");
    }
});
