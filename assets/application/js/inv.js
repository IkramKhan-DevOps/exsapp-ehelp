$(document).ready(function () {
    // -------------------------<< INITIALIZATIONS >>--------------------------------------
    let currentproduct = getIDFromUrl(document.URL);
    init();

    //-------------------------------------------------------------------------------------


    function init() {
        getApiWithParam(currentproduct);
    }

    // ----------------------------<< EVENTS >>-------------------------------------------
    $("#generate-barcode").click(function () {
        generatebarcode();
    });

    $("#cal-minus").click(function () {
        calculatepricing('minus', $('#pricein').val(), $('#priceout').val());
    });

    $("#cal-percent").click(function () {
        calculatepricing('percent', $('#pricein').val(), $('#priceout').val());
    });

    // ----------------------------<< METHODS >>-----------------------------------------
    function getIDFromUrl(customurl) {
        let index = customurl.split('/');
        return index[index.length - 2];
    }

    function calculatepricing(action, pricein, priceout) {
        if (pricein != '' || priceout != '') {
            if (action == 'percent') {
                $('#pricein').val(pricein - ((priceout * pricein) / 100));
            } else {
                $('#pricein').val(pricein - priceout);
            }
            $('#priceout').val(pricein);
        }
    }

    function generatebarcode() {
        $('#barcode').val('TB' + ((Math.floor(Math.random() * 999999999999) + 100000000).toString()));
    }

    // ----------------------------<< APICALLS >>----------------------------------------
    function getproductdetails() {

    }

    function getApiWithParam(param) {
        $.get('/api/product/' + param + '/', function () {
        }).done(function (data) {

            $('#name').val(data.name);
            $('#barcode').val(data.barcode);
            $('#desc').val(data.desc);
            $('#pricein').val(data.pricein);
            $('#priceout').val(data.priceout);
            $('#discount').val(data.discount);
            $('#salestax').val(data.salestax);
            $('#productstatus').html('<option value="' + data.productstatus + '">Available</option>');
            $('#activeshipment').prop('checked', data.activeshipment);

            $.get('/api/subcategories/', function () {
            }).done(function (datain) {
                let select;
                for (let i = 0; i < datain.length; i++) {
                    select = datain[i].id === data.subcategory ? 'selected' : '';
                    $('#subcategory').append('<option value="' + datain[i].id + '" ' + select + '>' + datain[i].name + '</option>');
                }
            });
            $('#likes').append(data.likes);
            $('#dislikes').append(data.dislikes);
            $('#created').text(data.created);
            $('#updated').text(data.updated);

        }).fail(function () {
        }).always(function () {
        });
    }

});
/*       $(document).ready(function () {

         initializations();

         // ------------------------INITIALIZATION_FUNCTION
         function initializations() {
             $('#attributes').hide();
             fetchcategories();
             fetchsubcategories($("#categories option:first").text());
         }

         // ------------------------EVENTS
         $("#categories").change(function () {
             fetchsubcategories($("#categories option:selected").text());
         });

         $("#subcategory").change(function () {
             fetchsubattributes($("#subcategry option:selected").text());
         });



         $('#form').submit(function () {
             var csrftoken = getCookie('csrftoken');
             $.ajax({
                 type: "POST",
                 url: "http://127.0.0.1:8000/inv/product/add/",
                 dataType: "json",
                 data: $('#form').serialize(),
                 headers: {"X-CSRFToken": csrftoken},
                 success: function (data, status) {
                     alert(status)
                 },
                 error: function (data, status) {
                     console.log(data);
                     console.log(status);
                 }
             });
             $(this).preventDefault();
         });

         // OUT _ FUNCTION

         function fetchcategories() {
             $.get('http://127.0.0.1:8000/public/categories/', function (categories, status) {
                 let categorieslist = '';
                 for (let index = 0; index < categories.length; index++) {
                     categorieslist += '<option value="' + categories[index].id + '">' + categories[index].name + '</option>';
                 }
                 $("#categories").html(categorieslist);
             });
         }

         function fetchsubcategories(category) {
             $.get('http://127.0.0.1:8000/public/subcategories/?category=' + category, function (subcategories, status) {
                 let subcategorieslist = '';
                 for (let index = 0; index < subcategories.length; index++) {
                     subcategorieslist += '<option value="' + subcategories[index].id + '">' + subcategories[index].name + '</option>';
                 }
                 $("#subcategory").html(subcategorieslist);
             });
         }

         function fetchsubattributes(subcategory) {
             $.get('http://127.0.0.1:8000/public/subattributes/?subcategory=' + subcategory, function (attributes, status) {
                 let output = '';
                 if (attributes.length > 0) {
                     for (let value = 0; value < attributes.length; value++) {
                         $('#attributes').show();
                         let attributedesc = attributes[value].attrribute.desc;
                         if (attributedesc == null) {
                             attributedesc = '';
                         }

                         output += '<div class="form-group">' +
                             '<p class=\'text-secondary pl-1\'>' + attributes[value].attrribute.name + '<br>' +
                             '<small class="light-text">' + attributedesc + '</small></p>' +
                             '<input type="text" class="form-control bg-light border-0" id="usr">' +
                             '</div>';
                     }
                     $('#attribute-values').html(output);
                 }
             });
         }




         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie !== '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = cookies[i].trim();
                     // Does this cookie string begin with the name we want?
                     if (cookie.substring(0, name.length + 1) === (name + '=')) {
                         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                         break;
                     }
                 }
             }
             return cookieValue;
         }

     });*/
