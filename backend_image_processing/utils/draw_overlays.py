import backend_image_processing.utils.business_logic as business_logic_module

def draw_overlays(frame, slot_statuses, available, total_slots):
        for roi, white, occupied in slot_statuses:
            business_logic_module.draw_slot_status(frame, roi, white, occupied)
        business_logic_module.overlay_available_count(frame, available, total_slots)
