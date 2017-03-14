/**
 * Created by Andrei on 3/13/2017.
 */

var docType = [
    {
        type: "LEGE",
        regex: new RegExp("proiect ([a-zA-Z]+\s?){1,3} ordonan", "i")
    },
    {
        type: "OUG",
        regex: new RegExp("ordonan\\S{1,2} de urgen\\S{1,2}", "i")
    },
    {
        type: "HG",
        regex: new RegExp("hot\S{1}r\S{1}re", "i")
    }
];

var titleStartMarkStrings = [
    "privind ",
    "pentru "
];

var titleEndMarkStrings = [
    "\n",
    "\r\n"
];

var titleEndMarkRegex = [
    new RegExp("sec\\S{1}iune", "i")
];

module.exports = {
    docType: docType,
    titleStartMarkStrings: titleStartMarkStrings,
    titleEndMarkStrings: titleEndMarkStrings,
    titleEndMarkRegex: titleEndMarkRegex
};