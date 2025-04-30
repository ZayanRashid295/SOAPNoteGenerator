import os
import asyncio
from api_clients import get_soap_notes
from comparison_engine import compare_soap_notes
from explanation_generator import generate_explanation
from pdf_generator import generate_final_soap_note_pdf, generate_analysis_report_pdf

CONVERSATION_FOLDER = 'conversations/'
OUTPUT_FOLDER = 'output/'

def setup_folders():
    os.makedirs(CONVERSATION_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def get_conversation_files():
    return [f for f in os.listdir(CONVERSATION_FOLDER) if f.endswith('.txt')]

async def process_conversation(conversation_file: str, idx: int, total: int):
    try:
        conversation_file_path = os.path.join(CONVERSATION_FOLDER, conversation_file)
        
        print(f"\nProcessing Conversation {idx}/{total}: {conversation_file}")
        print("-" * 80)
        
        # Read the conversation from file
        with open(conversation_file_path, 'r', encoding='utf-8') as file:
            conversation = file.read()

        # Generate SOAP notes from APIs
        print("Generating SOAP notes from APIs...")
        soap_notes = await get_soap_notes(conversation)
        
        if not soap_notes:
            print(f"Warning: No valid SOAP notes generated for {conversation_file}")
            return

        # Compare the generated SOAP notes
        print("Comparing SOAP notes...")
        comparison_result = compare_soap_notes(soap_notes)
        
        # Generate the explanation of comparison
        print("Generating analysis explanation...")
        explanation = generate_explanation(
            soap_notes,
            comparison_result['best_soap_note'],
            comparison_result['scores']
        )
        
        # Generate PDF reports
        print("Generating PDF reports...")
        generate_final_soap_note_pdf(comparison_result['best_soap_note'], idx)
        generate_analysis_report_pdf({
            'scores': comparison_result['scores'],
            'explanation': explanation
        }, idx)

        print(f"Successfully processed {conversation_file}")
        print(f"Output files generated in the 'output' folder")

    except AttributeError as e:
        print(f"Error processing {conversation_file}: {str(e)}")
        print("Hint: Check if a dictionary is being passed where a string is expected.")
    except Exception as e:
        print(f"Error processing {conversation_file}: {str(e)}")

async def main():
    try:
        setup_folders()
        conversation_files = get_conversation_files()
        
        if not conversation_files:
            print("No conversation files found in the 'conversations' folder.")
            return
        
        # Process all the conversation files concurrently
        tasks = [
            process_conversation(file, idx, len(conversation_files))
            for idx, file in enumerate(conversation_files, start=1)
        ]
        
        await asyncio.gather(*tasks)

    except Exception as e:
        print(f"An error occurred in main: {str(e)}")
    finally:
        # Ensure to cancel all remaining tasks
        tasks = [task for task in asyncio.all_tasks() if task is not asyncio.current_task()]
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)

if __name__ == "__main__":
    # Make sure to run the asynchronous main function
    asyncio.run(main())
