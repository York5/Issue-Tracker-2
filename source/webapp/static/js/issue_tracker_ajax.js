$.ajax({
    data: JSON.stringify({username: 'mike', password: '1234'}),
    method: 'post',
    url: "http://localhost:8000/api/v2/login/",
    contentType: 'application/json',
    dataType: 'json',
	success: function(response, status){
        localStorage.setItem('apiToken', response.token);
        console.log(response);
        allProjects();
        allIssues();
        allProjectIssues();
        projectCreate();
        projectDelete();
        },
	error: function(response, status) {console.log(response);},
});


// Вывод всех проектов:
function allProjects() {
    $.ajax({
        method: 'get',
        url: "http://localhost:8000/api/v2/projects/",
        headers: {'Authorization': 'Token ' + localStorage.getItem('apiToken')},
        dataType: 'json',
        success: function(response, status) {
            console.log('Все проекты: ');
            console.log(response);},
        error: function(response, status) {
            console.log('Ошибки Вывода всех Проектов: ');
            console.log(response);},
    });
}


// Вывод всех задач:
function allIssues() {
    $.ajax({
        method: 'get',
        url: "http://localhost:8000/api/v2/issues/",
        headers: {'Authorization': 'Token ' + localStorage.getItem('apiToken')},
        dataType: 'json',
        success: function(response, status) {
            console.log('Все Задачи: ');
            console.log(response);},
        error: function(response, status) {
            console.log('Ошибки вывода всех Задач: ');
            console.log(response);},
    });
}


// Вывод задач указанного проекта:
function allProjectIssues() {
    $.ajax({
        method: 'get',
        url: "http://localhost:8000/api/v2/issues/?project=1",
        headers: {'Authorization': 'Token ' + localStorage.getItem('apiToken')},
        dataType: 'json',
        success: function(response, status) {
            console.log('Все Задачи Указанного Проекта: ');
            console.log(response);},
        error: function(response, status) {
            console.log('Ошибки Вывода Задач Проекта: ');
            console.log(response);},
    });
}


// Создание проекта:
function projectCreate() {
    $.ajax({
        data: JSON.stringify({
            "name": "New Project From API",
            "description": "This is a Project, created via ajax request, with authorization by Token",
            "status": "active",
            "users": [10, 9] 
        }),
        method: 'post',
        url: "http://localhost:8000/api/v2/projects/",
        headers: {'Authorization': 'Token ' + localStorage.getItem('apiToken')},
        dataType: 'json',
        contentType: 'application/json',
        success: function(response, status) {
            console.log('Создание проекта: ');
            console.log(response);},
        error: function(response, status) {
            console.log('Ошибки создания проекта: ');
            console.log(response);},
    });
}


// Удаление проекта:
function projectDelete() {
    $.ajax({
        method: 'delete',
        url: "http://localhost:8000/api/v2/projects/20",
        headers: {'Authorization': 'Token ' + localStorage.getItem('apiToken')},
        dataType: 'json',
        success: function(response, status) {
            console.log('Удаление проекта: ');
            console.log(response);},
        error: function(response, status) {
            console.log('Ошибки Удаления проекта: ');
            console.log(response);},
    });
}



// let tokens = {}

// $.ajax({
//     data: JSON.stringify({username: 'mike', password: '1234'}),
//     method: 'post',
//     url: "http://localhost:8000/api/v2/login/",
//     contentType: 'application/json',
//     dataType: 'json',
// 	success: function(response, status){
//         tokens.myToken = response.token;
//         console.log(response);
//         },
// 	error: function(response, status) {console.log(response);},
// });

// $.ajax({
//     method: 'get',
//     url: "http://localhost:8000/api/v2/projects/",
// 	headers: {'Authorization': 'Token ' + tokens.myToken},
//     dataType: 'json',
// 	success: function(response, status) {console.log(response);},
// 	error: function(response, status) {console.log(response);},
// });
