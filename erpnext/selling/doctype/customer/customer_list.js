frappe.listview_settings["Customer"] = {
	add_fields: ["customer_name", "territory", "customer_group", "customer_type", "image"],
};

frappe.listview_settings['Customer'].get_indicator = function(doc) {
	console.log (doc)
	// your logic
	if (doc.status === "Active") {
		return [__('Active'), 'green']
	}
	else if (doc.status === "Service Completed") {
		return [__('Service Completed'), 'grey']
	}
	else if (doc.status === "Maintaining Relationship") {
		return [__('Maintaining Relationship'), 'green']
	}
	else if (doc.status === "Renewed") {
		return [__('Renewed'), 'green']
	}
	else if (doc.status === "Dormant") {
		return [__('Dormant'), 'orange']
	}
	else if (doc.status === "Closed") {
		return [__('Closed'), 'red']
	}
}

