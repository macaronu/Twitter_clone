// like function
$(".ajax-like").click(function (e) {
  e.preventDefault();
  var tweetid = $(this).attr("name");
  $.ajax({
    type: "POST",
    url: url,
    data: {
      tweetid: tweetid,
      csrfmiddlewaretoken: csrftoken,
    },
    dataType: "json",
    success: function (response) {
      selector = document.getElementsByName(response.tweetid);
      $(selector).children("#like-count").html(response.like_count);
      if (response.method == "create") {
        $(selector).children("#heart").removeClass("far myhrt");
        $(selector).children("#heart").addClass("fas myhrt-red");
        $(selector).children("#like-count").addClass("red");
      } else if (response.method == "delete") {
        $(selector).children("#heart").removeClass("fas myhrt-red");
        $(selector).children("#heart").addClass("far myhrt");
        $(selector).children("#like-count").removeClass("red");
      }
    },
  });
});
