function redirect(elem) {
  window.location.href = $(elem).find('a').attr('href');
}

function Retrieve(event, page, faculty, specialization) {
    event.stopPropagation();
    event.preventDefault();
    var data = {};
    data["page"] = page;
    data["faculty"] = faculty;
    if (specialization) {
      data["specialization"] = specialization;
    }
    $.ajax({
      url: "/get_students",
      type: "get",
      data: data,
      success: function(data) {
        $("#container").empty();
        $("#container").html(data);
      }
    });
  }

  $("#name").keyup(function() {
    var name = "", surname = "";
    var content = $("#container").html();
    if ($.trim($("#name").val()).length == 0) {
      $("#container").empty();
      $.ajax({
        url: "search/",
        type: "GET",
        data: {
          'name': "-1",
          'surname': "-1"
        },
        success: function (data) {
          $("#container").html(data);
        }
      });
    }
    var str = $("#name").val().split(" ");
    if (str.length > 0) name = str[0];
    if (str.length > 1) surname = str[1];

    if (name && name.length > 0) name = name[0].toUpperCase() + name.slice(1);
    if (surname && surname.length > 0) surname = surname[0].toUpperCase() + surname.slice(1);


    $.ajax({
      url: "http://127.0.0.1:8000/search/",
      type: "GET",
      data: {
        'name': name,
        'surname': surname
      },
      success: function (data) {
        $("#container").html(data);
      }
    });
  });


  function addReview(name, surname) {
    var val = $("#textarea1").val();
    if (val.length === 0)
      return false;
    $.ajax({
      url : "/add_rev",
      type: "get",
      data : {
        'content': val,
        'name' : name,
        'surname' : surname
      },
      success: function(data) {
        $("#textarea1").val("");
        $("#reviews").empty();
        $("#reviews").html(data);
      }
    });
  }

  function addStudents(current) {
    if (current.checked) {
      $.ajax({
        url: "/get_students",
        type: "get",
        data : {
          'specialization': current.id,
          'page': '1',
        },
        success: function(data) {
          $("#container").empty();
          $("#container").html(data);
        },
        error: function(data) {

        }
      });
    }
  }

  function addSpecializations(current) {
    if (current.checked) {
      $.ajax({
        url: "/get_specialization",
        type: "get",
        data : {
          'faculty' : $.trim(current.id),
        },
        dataType: 'text',
        success: function (data) {
          $(".all-specializations").empty();
          $(".all-specializations").append(data);
        },
        error: function(jhr){

        }
      });

      $.ajax({
        url: "/get_students_by_faculty",
        type: "get",
        data : {
          'faculty': $.trim(current.id),
          'page': 1,
        },
        success: function(data) {
          $("#container").empty();
          $("#container").html(data);
        },
        error: function(data) {

        }
      });
    }
  }
