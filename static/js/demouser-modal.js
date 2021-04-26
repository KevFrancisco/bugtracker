$(document).ready(function() {
    $('a[data-confirm]').click(function(ev) {
        var href = $(this).attr('href');
        if (!$('#dataConfirmModal').length) {
            $('body').prepend('<div id="dataConfirmModal" class="modal fade" role="dialog" aria-labelledby="dataConfirmLabel" aria-hidden="true"> <div class="modal-dialog modal-dialog-centered"> <div class="modal-content"> <div class="modal-header"> <h3 id="dataConfirmLabel" class="m-0"> Demo Access </h3> <button type="button" class="close" data-dismiss="modal" aria-label="Close"> <span aria-hidden="true">&times;</span> </button> </div> <div id="modal-body" class="bg-darker modal-body my-3"></div> <div class="mb-3"> <ul class="mx-5 mb-5 border lead text-center list-group"> <li class="list-group-item m-1"><div class="h3 my-auto">Admin</div><div class="text-nowrap"><span class="small text-muted">username: </span>demoadmin<br><span class="small text-muted">password:</span> demo </div></li> <li class="list-group-item m-1"><div class="h3 my-auto">Submitter</div><div class="text-nowrap"><span class="small text-muted">username: </span>demosub<br><span class="small text-muted">password:</span> demo </div></li> <li class="list-group-item m-1"><div class="h3 my-auto">Developer</div><div class="text-nowrap"><span class="small text-muted">username: </span>demodev<br><span class="small text-muted">password:</span> demo </div></li> <li class="list-group-item m-1"><div class="h3 my-auto">Project Manager</div><div class="text-nowrap"><span class="small text-muted">username: </span>demopm<br><span class="small text-muted">password:</span> demo </div></li> </ul> </div> <div class="modal-footer"> <button class="btn btn-success" data-dismiss="modal" aria-hidden="true"> Okay </button> </div> </div> </div> </div>');
        } 
        $('#dataConfirmModal').find('#modal-body').text($(this).attr('data-confirm'));
        $('#dataConfirmOK').attr('href', href);
        $('#dataConfirmModal').modal({show:true});
        return false;
    });
});