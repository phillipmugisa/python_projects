document.addEventListener('DOMContentLoaded', () => {

    var create_task = document.querySelector('.create-task')
    var tasks = document.querySelector('.tasks')
    var task_create = document.getElementById('task-create')
    var view_create = document.getElementById('view-create')

    task_create.addEventListener('click', () => {
        tasks.style.display = 'none'
        create_task.style.display = 'block'
    })
    view_create.addEventListener('click', () => {
        tasks.style.display = 'block'
        create_task.style.display = 'none'
    })

})