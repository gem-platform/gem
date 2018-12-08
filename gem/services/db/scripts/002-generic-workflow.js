// Create stages for "Generic Workflow"
stageInitial = db.workflowStages.insertOne({
    name: "Initial",
    description: "Initial stage. No actions required.",
    actions: []
})

stageReview = db.workflowStages.insertOne({
    name: "Review",
    description: "Review.",
    actions: [
        { id: "acquaintance" },
        { id: "comments" },
        { id: "discussion" },
        { id: "ballot" },
        { id: "ballot.results" }
    ]
})

stageDone = db.workflowStages.insertOne({
    name: "Done",
    description: "Workflow completed. No actions required.",
    actions: []
})

// Create "Generic Workflow"
workflow = db.workflowTypes.insertOne({
    name: "Generic Workflow",
    stages: [
        stageInitial.insertedId,
        stageReview.insertedId,
        stageDone.insertedId
    ]
});
