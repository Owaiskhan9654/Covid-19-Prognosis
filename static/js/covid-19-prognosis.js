$(document).ready(function () {

    $('#result-heading').hide();
    $('#result-row').hide();

    var onCompletion = (res) => {
        var result;
        if(res.class==1){
            let prob = res.probability;
            $('#result').removeClass('text-success').addClass('text-danger');
            result=`Based on the features given model, you are ${(prob*100).toFixed(2)}% likely to have SARS COVID-19.`
        }
        else{
            $('#result').removeClass('text-danger').addClass('text-success');
            result=`Based on the features given, you are unlikely to have SARS COVID-19`
        }
        $('#result').html(result);
        $('#result-row').show();
        $('#result-heading').show();
    }   

    $('form[name="Covid-19-prognosis-form"]').submit(function (event) {
        event.preventDefault();
        var form = $('form[name="Covid-19-prognosis-form"]')[0];
        if (form.checkValidity() === false) {
            console.log('Not valid!!')
            return;
        }
        else{
            let form_data = new FormData();
            console.log(("#coughid").val())
            console.log($('select[name="fever"]').val())
            console.log($('input[name="sore_throat"]').val())
            console.log($('input[name="shortness_in_breath"]').val())
            console.log($('input[name="head_ache"]').val())
            console.log($('input[name="sex"]').val())
            console.log($('input[name="age"]').val())
            console.log($('input[name="vaccinated"]').val())

            form_data.append('cough', $('input[name="cough"]'));
            form_data.append('fever', $('input[name="fever"]').val());
            form_data.append('sore_throat', $('input[name="sore_throat"]').val());
            form_data.append('shortness_in_breath', $('input[name="shortness_in_breath"]').val());
            form_data.append('head_ache', $('input[name="head_ache"]').val());
            form_data.append('sex', $('input[name="sex"]').val());
            form_data.append('age', $('input[name="age"]').val());
            form_data.append('vaccinated', $('input[name="vaccinated"]').val());

            $.ajax({
                type: 'POST',
                data: form_data,
                processData: false,
                contentType: false,
                url: '/prognosis/covid_19'
            }).done(function(response){
                onCompletion(response);
            });
        }

    });

});