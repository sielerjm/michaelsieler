certificate_section <- function(xlsx = "data/cv.xlsx", sheet = "awards", page_break_after = FALSE, colour = "#3f007d") {
    text <- read_excel_sheet(xlsx, sheet)[
        i = .N:1,
        j = sprintf(
            "### %s\n\n%s\n\n%s\n\n::: aside\n*[%s](%s)*\n:::\n\n\n\n",
            name, institute, description, paste0(fontawesome::fa("link", fill = colour), " ", website), url
        )
    ]
    
    if (page_break_after) {
        c(sprintf("## Awards (%s) {data-icon=trophy .break-after-me}", length(text)), text)
    } else {
        c(sprintf("## Awards (%s) {data-icon=trophy}", length(text)), text)
    }
}
