function createPageChooserOrCreate(id, pageTypes, openAtParentId, canChooseRoot) {
    var createElement = $('#' + id + '-create');
    var chooseElement = $('#' + id + '-chooser .unchosen .action-choose');

    createElement.change(function() {
        if (createElement.is(':checked')) {
            chooseElement.hide();
        } else {
            chooseElement.show();
        }
    });
}
