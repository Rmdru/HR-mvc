//load more bttn
$(document).ready(function() {
    if ($(".data_types_page, .null_values_page, .special_characters_page").length > 0) {
        var visibleRows = 0;

        if ($(".row").length < 5) {
            $(".loadMoreBttn").hide();
        }
        
        $(window).on("load", function() {
            $(".row.displayNone").each(function(i) {
                if (i < 5) {
                    $(this).removeClass("displayNone");
                    visibleRows++;
                }
            })
        })
        
        $(".loadMoreBttn").on("click", function() {
            $(".row.displayNone").each(function(i) {
                if (i < 5) {
                    $(this).removeClass("displayNone");
                    visibleRows++;
                }
                
                if (visibleRows == $(".row").length) {
                    $(".loadMoreBttn").hide();
                }
            })
        })
    }
})