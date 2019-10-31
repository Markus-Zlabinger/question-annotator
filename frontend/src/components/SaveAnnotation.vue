<template>
    <span></span>
</template>

<script>
    import axios from "axios";

    export default {
        name: "SaveAnnotation",
        methods: {
            change_annotation(candidate, qid, answerlabels) {
                if (answerlabels.length === 0) {
                    this.errorToast("Select at least one answer label!");
                    return false;
                }

                const url = "http://127.0.0.1:5000/modifyannotation";
                const formData = new FormData();

                answerlabels.forEach(aid => {
                    formData.append("labels[]", aid);
                });
                formData.append("qid", qid);

                return axios
                    .post(url, formData)
                    .then(response => {
                        this.successToast3(candidate);
                    })
                    .catch(e => {
                        this.errorToast("Something went wrong! Please try again later.");
                    });
            },
            save_annotation(candidate, answerlabels, questionlabels) {
                if (answerlabels.length === 0) {
                    this.errorToast("Select at least one answer label!");
                    window.scrollTo(0, 0);
                    return false;
                }
                if (questionlabels.length === 0) {
                    this.errorToast("Select at least one question to label!");
                    window.scrollTo(0, 0);
                    return false;
                }

                const url = "http://127.0.0.1:5000/saveannotation";
                const formData = new FormData();

                answerlabels.forEach(aid => {
                    formData.append("labels[]", aid);
                });
                questionlabels.forEach(qid => {
                    formData.append("questionlist[]", qid);
                });
                return axios
                    .post(url, formData)
                    .then(response => {
                        if (questionlabels.length > 1) {
                            this.successToast(candidate, questionlabels.length - 1, answerlabels);
                        } else {
                            this.successToast2(candidate, answerlabels);
                        }
                        window.scrollTo(0, 0);
                    })
                    .catch(e => {
                        this.errorToast("Something went wrong! Please try again later.");
                    });
            },
            errorToast(msg) {
                const h = this.$createElement
                const vNodesMsg = h(
                    'p',
                    [
                        msg,
                    ]
                );
                this.$bvToast.toast([vNodesMsg], {
                    title: "Annotation Failed",
                    variant: "danger",
                    solid: true,
                    autoHideDelay: 3000,
                })
            },
            successToast(candidate, numAnnotations, answerlabels) {
                const h = this.$createElement
                const vNodesMsg = h(
                    'p',
                    [
                        'The candidate  ',
                        h('strong', {}, candidate),
                        ' and ',
                        h('strong', {}, numAnnotations),
                        ' other questions were annotated with the labels: ',
                        h('strong', {}, answerlabels.join(" ~ ")),

                    ]
                );

                // this.$bvToast.toast("The candidate <b>" + candidate + "</b> and " + numAnnotations + ' other questions were annotated.', {
                this.$bvToast.toast([vNodesMsg], {
                    title: "Annotation Successful",
                    variant: "success",
                    solid: true,
                    autoHideDelay: 3000,
                })
            },
            successToast2(candidate, answerlabels) {
                const h = this.$createElement
                const vNodesMsg = h(
                    'p',
                    [
                        'The candidate  ',
                        h('strong', {}, candidate),
                        ' was annotated with the labels: ',
                        h('strong', {}, answerlabels.join(" ~ ")),

                    ]
                );

                // this.$bvToast.toast("The candidate <b>" + candidate + "</b> and " + numAnnotations + ' other questions were annotated.', {
                this.$bvToast.toast([vNodesMsg], {
                    title: "Annotation Successful",
                    variant: "success",
                    solid: true,
                    autoHideDelay: 3000,
                })
            },
            successToast3(candidate) {
                const h = this.$createElement
                const vNodesMsg = h(
                    'p',
                    [
                        'The label for the candidate  ',
                        h('strong', {}, candidate),
                        ' was changed.'
                    ]
                );
                this.$bvToast.toast([vNodesMsg], {
                    title: "Annotation Successful",
                    variant: "success",
                    solid: true,
                    autoHideDelay: 3000,
                })
            }
        }
    }


</script>

<style scoped>

</style>