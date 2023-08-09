async def convert_to_qcl(item_data):
    qcl_transaction_data = {
        "qcl_transaction_number": None,
        "qcl_transaction_type_name": None
    }

    general_obj = {
        "qcl_category": "Accounting",
        "qcl_subcategory": "CrossConnect",
        "qcl_transaction_data": qcl_transaction_data,
        "qcl_source_id": "ONS",
        "qcl_destination_id": "EQX"
    }

    transaction_specific_obj = {
        "generic_fields": {
            "time_initiated": None,
            "lattice_user_id": None
        }
    }

    source_specific_fields = {
        "qcl_a_side_details": {
            "qcl_cc_patch_panel_id": item_data.get('custitem_patch_panel_a').get('refName'),
            "qcl_cc_connection_service": item_data.get('custitem_connection_service').get('refName'),
            "qcl_cc_media_type": item_data.get('custitem_media_type').get('refName'),
            "qcl_cc_protocol_type": item_data.get('custitem_protocol_type').get('refName'),
            "qcl_cc_connector_type": item_data.get("custitem_a_side_connector_type").get('refName'),
            "qcl_cc_patch_panel_port_a": item_data.get('custitem_patch_panel_a_port_a', None),
            "qcl_cc_patch_panel_port_b": item_data.get('custitem_patch_panel_b_port_b', None)
        },
        "qcl_z_side_details": {
            "qcl_cc_patch_panel_id": item_data.get('custitem_patch_panel_z'),
            "qcl_cc_connector_type": item_data.get('custitem_z_side_connector_type').get('refName'),
            "qcl_cc_patch_panel_port_a": item_data.get('custitem_patch_panel_z_port_a', None),
            "qcl_cc_patch_panel_port_b": item_data.get('custitem_patch_panel_z_port_b', None),
            "qcl_cc_loa": None
        },
        "qcl_cc_order_contacts": {
            "qcl_cc_contacts": None
        },
        "qcl_cc_media_convertor_required": item_data.get('custitem_media_converter_required', None).get('refName')
    }

    qcl_data_obj = {
        "general_obj": general_obj,
        "transaction_specific_obj": transaction_specific_obj
    }
    return qcl_data_obj


# mandatory_parameters = {
#     "qcl_a_side_details": {
#             "qcl_cc_patch_panel_id": item_data.get('custitem_patch_panel_a').get('refName'),
#             "qcl_cc_connection_service": item_data.get('custitem_connection_service').get('refName'),
#             "qcl_cc_media_type": item_data.get('custitem_media_type').get('refName'),
#             "qcl_cc_protocol_type": item_data.get('custitem_protocol_type').get('refName'),
#             "qcl_cc_connector_type": item_data.get("custitem_a_side_connector_type").get('refName'),
#              },
#         "qcl_z_side_details": {
#             "qcl_cc_patch_panel_id": item_data.get('custitem_patch_panel_z'),
#             "qcl_cc_connector_type": item_data.get('custitem_z_side_connector_type').get('refName'),

# }} 