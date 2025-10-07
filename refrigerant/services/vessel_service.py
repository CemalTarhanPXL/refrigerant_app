from django.db import transaction
from django.db.models import F
from ..models import Vessel 
from django.core.management.base import BaseCommand 

_command_stdout_writer = BaseCommand()


def withdraw_refrigerant(user_name: str, vessel_id: int, amount: float):
    """
    Voer een thread-safe en gecontroleerde opname van koelmiddel uit.
    Geeft een tuple terug: (succes: bool, bericht: str)
    """
    
    try:
        with transaction.atomic():
            vessel = Vessel.objects.select_for_update().get(id=vessel_id)
            if vessel.content < amount:
                message = f"{user_name}: Kan niet {amount} kg opnemen. Vat (ID:{vessel_id}) is leeg of te laag. Huidige inhoud: {vessel.content} kg."
                return False, _command_stdout_writer.style.WARNING(message)
            Vessel.objects.filter(id=vessel_id).update(content=F('content') - amount)
            message = f"{user_name}: Succesvol {amount} kg opgenomen. Nieuwe inhoud: {vessel.content - amount} kg."
            return True, _command_stdout_writer.style.SUCCESS(message)
            
    except Vessel.DoesNotExist:
        message = f"{user_name}: Fout, Vat (ID:{vessel_id}) niet gevonden."
        return False, _command_stdout_writer.style.ERROR(message)
    except Exception as e:
        message = f"{user_name}: Onbekende fout bij opname: {e}"
        return False, _command_stdout_writer.style.ERROR(message)