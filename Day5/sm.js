let students = [];

function addStudent() {
    const name = document.getElementById('name').value.trim();
    const marks = Number(document.getElementById('marks').value);

    if (!name || Number.isNaN(marks)) {
        alert('Please enter a valid name and marks.');
        return;
    }

    students.push({
        name: name,
        marks: marks
    });

    document.getElementById('name').value = '';
    document.getElementById('marks').value = '';
    displayStudents();
}

function displayStudents() {
    const table = document.getElementById('studentList');
    table.innerHTML = '';

    let total = 0;

    students.forEach(student => {
        const status = Number(student.marks) >= 35 ? 'Pass' : 'Fail';
        total += Number(student.marks);

        table.innerHTML += `
            <tr>
                <td>${student.name}</td>
                <td>${student.marks}</td>
                <td>${status}</td>
            </tr>
        `;
    });

    const average = students.length > 0 ? total / students.length : 0;
    document.getElementById('total').textContent = total;
    document.getElementById('average').textContent = average;
}