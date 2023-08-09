from typing import Dict

from app import logger

log = logger.get_logger()


class ObjectMapping:

    @staticmethod
    async def qcl_to_equinox(data) -> Dict:
        """
        Conversion of data from qcl to equinox
        :param data: input qcl request body.
        :return: dict object
        """
        log.info(f"Qcl data from the micro-service 3 before mapping -> {data}")
        parent_obj = data.get("qcl_cc_details").get("source_specific_fields")
        equinox_payload = {
            "customerReferenceId": "C1111",
            "description": "Please provide any additional details the technician may need to complete your request.",
            "details": [
                {
                    "aSide": {
                        "connectionService": parent_obj.get("qcl_a_side_details").get("qcl_cc_connection_service"),
                        "mediaType": parent_obj.get("qcl_a_side_details").get("qcl_cc_media_type"),
                        "protocolType": parent_obj.get("qcl_a_side_details").get("qcl_cc_protocol_type"),
                        "connectorType": parent_obj.get("qcl_a_side_details").get("qcl_cc_connector_type"),
                        "patchPanel": {
                            "id": parent_obj.get("qcl_a_side_details").get("qcl_cc_patch_panel_id")

                        }
                    },
                    "zSide": {
                        "connectorType": parent_obj.get("qcl_z_side_details").get("qcl_cc_connector_type"),
                        "patchPanel": {
                            "id": parent_obj.get("qcl_z_side_details").get("qcl_cc_patch_panel_id")
                        }
                    }
                }
            ]
        }

        if parent_obj.get("qcl_a_side_details").get("qcl_cc_patch_panel_port_a") is not None:
            equinox_payload["details"][0]["aSide"]["patchPanel"]["portA"] = parent_obj.get("qcl_a_side_details").get(
                "qcl_cc_patch_panel_port_a")
        if parent_obj.get("qcl_a_side_details").get("qcl_cc_patch_panel_port_b") is not None:
            equinox_payload["details"][0]["aSide"]["patchPanel"]["portB"] = parent_obj.get("qcl_a_side_details").get(
                "qcl_cc_patch_panel_port_b")
        if parent_obj.get("qcl_z_side_details").get("qcl_cc_patch_panel_port_a") is not None:
            equinox_payload["details"][0]["zSide"]["patchPanel"]["portA"] = parent_obj.get("qcl_z_side_details").get(
                "qcl_cc_patch_panel_port_a")
        if parent_obj.get("qcl_z_side_details").get("qcl_cc_patch_panel_port_b") is not None:
            equinox_payload["details"][0]["zSide"]["patchPanel"]["portB"] = parent_obj.get("qcl_z_side_details").get(
                "qcl_cc_patch_panel_port_b")
        log.info(f"Payload for equinox purchase/create order after mapping -> {equinox_payload}")
        return equinox_payload


map_obj = ObjectMapping()
