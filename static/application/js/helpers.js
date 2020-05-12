function getIDFromUrl(customurl) {
    let index = customurl.split('/');
    return index[index.length - 2];
}

function get_api_data(url, method) {
    $.ajax({
        url: url,
        type: method,
        contentType: false,
        processData: false
    }).then(function (data, status) {
        return data;
    }).cache(function (error) {
        return error;
    });
}