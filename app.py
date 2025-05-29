{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyN7jl7L32bwmWcibPnr8msh",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/theyashyadav001/To-do-list/blob/main/app.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "from google.colab import drive\n",
        "drive.mount('/content/drive')\n"
      ],
      "metadata": {
        "id": "J0bsDyfviIMy",
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "f89b5030-f88e-41b9-b0e4-60e0b5c71cfa"
      },
      "execution_count": 6,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Mounted at /content/drive\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import json\n",
        "import os\n",
        "\n",
        "# Path to store tasks\n",
        "file_path = \"/content/drive/MyDrive/todo_tasks.json\"\n",
        "\n",
        "# Load existing tasks\n",
        "if os.path.exists(file_path):\n",
        "    with open(file_path, \"r\") as file:\n",
        "        tasks = json.load(file)\n",
        "else:\n",
        "    tasks = []\n",
        "\n",
        "def save_tasks():\n",
        "    with open(file_path, \"w\") as file:\n",
        "        json.dump(tasks, file)\n"
      ],
      "metadata": {
        "id": "BFACOunYkEde"
      },
      "execution_count": 7,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "from datetime import datetime\n",
        "\n",
        "def update_display(sort_by=\"None\"):\n",
        "    if not tasks:\n",
        "        return \"📭 No tasks yet.\"\n",
        "\n",
        "    sorted_tasks = tasks.copy()\n",
        "\n",
        "    if sort_by == \"Due Date\":\n",
        "        # Sort by due date (oldest first)\n",
        "        def parse_date(task):\n",
        "            try:\n",
        "                return datetime.strptime(task[\"due\"], \"%Y-%m-%d\")\n",
        "            except:\n",
        "                return datetime.max\n",
        "        sorted_tasks.sort(key=parse_date)\n",
        "\n",
        "    elif sort_by == \"Priority\":\n",
        "        # Define priority order\n",
        "        priority_order = {\"High\": 0, \"Medium\": 1, \"Low\": 2}\n",
        "        sorted_tasks.sort(key=lambda x: priority_order.get(x[\"priority\"], 3))\n",
        "\n",
        "    # Display\n",
        "    output = \"\"\n",
        "    for i, task in enumerate(sorted_tasks):\n",
        "        status = \"✅\" if task[\"done\"] else \"❌\"\n",
        "        output += f\"{i}. {task['task']} (Due: {task['due']}, Priority: {task['priority']}) [{status}]\\n\"\n",
        "    return output\n"
      ],
      "metadata": {
        "id": "1QxS_fOlkRQp"
      },
      "execution_count": 9,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "import json\n",
        "import os\n",
        "from datetime import datetime\n",
        "import gradio as gr\n",
        "\n",
        "# File path in Google Drive\n",
        "file_path = \"/content/drive/MyDrive/todo_tasks.json\"\n",
        "\n",
        "# Load tasks\n",
        "if os.path.exists(file_path):\n",
        "    with open(file_path, \"r\") as f:\n",
        "        tasks = json.load(f)\n",
        "else:\n",
        "    tasks = []\n",
        "\n",
        "def save_tasks():\n",
        "    with open(file_path, \"w\") as f:\n",
        "        json.dump(tasks, f)\n",
        "\n",
        "def add_task(task_text, due_date, priority):\n",
        "    if task_text.strip() != \"\":\n",
        "        tasks.append({\n",
        "            \"task\": task_text.strip(),\n",
        "            \"due\": due_date.strip(),\n",
        "            \"priority\": priority,\n",
        "            \"done\": False\n",
        "        })\n",
        "        save_tasks()\n",
        "    return update_display(\"None\")\n",
        "\n",
        "def mark_done(index):\n",
        "    if 0 <= index < len(tasks):\n",
        "        tasks[index][\"done\"] = True\n",
        "        save_tasks()\n",
        "    return update_display(\"None\")\n",
        "\n",
        "def delete_task(index):\n",
        "    if 0 <= index < len(tasks):\n",
        "        tasks.pop(index)\n",
        "        save_tasks()\n",
        "    return update_display(\"None\")\n",
        "\n",
        "def update_display(sort_by=\"None\"):\n",
        "    if not tasks:\n",
        "        return \"📭 **No tasks yet.**\"\n",
        "\n",
        "    sorted_tasks = tasks.copy()\n",
        "\n",
        "    if sort_by == \"Due Date\":\n",
        "        def parse_date(task):\n",
        "            try:\n",
        "                return datetime.strptime(task[\"due\"], \"%Y-%m-%d\")\n",
        "            except:\n",
        "                return datetime.max\n",
        "        sorted_tasks.sort(key=parse_date)\n",
        "\n",
        "    elif sort_by == \"Priority\":\n",
        "        priority_order = {\"High\": 0, \"Medium\": 1, \"Low\": 2}\n",
        "        sorted_tasks.sort(key=lambda x: priority_order.get(x[\"priority\"], 3))\n",
        "\n",
        "    output = \"### 📋 To-Do List\\n\\n\"\n",
        "    for i, task in enumerate(sorted_tasks):\n",
        "        status = \"✅\" if task[\"done\"] else \"❌\"\n",
        "        color = \"🟥\" if task[\"priority\"] == \"High\" else \"🟨\" if task[\"priority\"] == \"Medium\" else \"🟩\"\n",
        "        output += f\"**{i}. {task['task']}**  \\nDue: `{task['due']}` | Priority: {color} {task['priority']} | Status: {status}\\n\\n\"\n",
        "    return output\n"
      ],
      "metadata": {
        "id": "-Aw-ZJXTk9aw"
      },
      "execution_count": 11,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "import gradio as gr\n",
        "\n",
        "with gr.Blocks() as demo:\n",
        "    gr.Markdown(\"## 📝 Advanced To-Do List with Sorting\")\n",
        "\n",
        "    with gr.Row():\n",
        "        task_input = gr.Textbox(label=\"Task\")\n",
        "        due_input = gr.Textbox(label=\"Due Date (YYYY-MM-DD)\")\n",
        "        priority_input = gr.Dropdown([\"Low\", \"Medium\", \"High\"], label=\"Priority\")\n",
        "        add_button = gr.Button(\"Add Task\")\n",
        "\n",
        "    output_display = gr.Textbox(label=\"Tasks\", lines=12)\n",
        "\n",
        "    sort_by = gr.Dropdown([\"None\", \"Due Date\", \"Priority\"], label=\"Sort Tasks By\")\n",
        "    sort_button = gr.Button(\"Apply Sort\")\n",
        "\n",
        "    with gr.Row():\n",
        "        done_index = gr.Number(label=\"Mark Done (Task #)\", precision=0)\n",
        "        done_button = gr.Button(\"Mark as Done\")\n",
        "\n",
        "    with gr.Row():\n",
        "        delete_index = gr.Number(label=\"Delete Task (Task #)\", precision=0)\n",
        "        delete_button = gr.Button(\"Delete Task\")\n",
        "\n",
        "    # Function to update with sorting\n",
        "    def apply_sorting(sort_option):\n",
        "        return update_display(sort_option)\n",
        "\n",
        "    # Connect actions\n",
        "    add_button.click(add_task, [task_input, due_input, priority_input], output_display)\n",
        "    done_button.click(mark_done, done_index, output_display)\n",
        "    delete_button.click(delete_task, delete_index, output_display)\n",
        "    sort_button.click(apply_sorting, sort_by, output_display)\n",
        "\n",
        "demo.launch()\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 645
        },
        "id": "UTx-hZNplO28",
        "outputId": "dd89aa7e-b23b-4413-d41f-f18d90b3f970"
      },
      "execution_count": 12,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "It looks like you are running Gradio on a hosted a Jupyter notebook. For the Gradio app to work, sharing must be enabled. Automatically setting `share=True` (you can turn this off by setting `share=False` in `launch()` explicitly).\n",
            "\n",
            "Colab notebook detected. To show errors in colab notebook, set debug=True in launch()\n",
            "* Running on public URL: https://9107b9e4220371833d.gradio.live\n",
            "\n",
            "This share link expires in 1 week. For free permanent hosting and GPU upgrades, run `gradio deploy` from the terminal in the working directory to deploy to Hugging Face Spaces (https://huggingface.co/spaces)\n"
          ]
        },
        {
          "output_type": "display_data",
          "data": {
            "text/plain": [
              "<IPython.core.display.HTML object>"
            ],
            "text/html": [
              "<div><iframe src=\"https://9107b9e4220371833d.gradio.live\" width=\"100%\" height=\"500\" allow=\"autoplay; camera; microphone; clipboard-read; clipboard-write;\" frameborder=\"0\" allowfullscreen></iframe></div>"
            ]
          },
          "metadata": {}
        },
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": []
          },
          "metadata": {},
          "execution_count": 12
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "file_path = \"todo_tasks.json\"\n"
      ],
      "metadata": {
        "id": "32aSmiZSlRY-"
      },
      "execution_count": 13,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [],
      "metadata": {
        "id": "Hr7r8QyjmBAJ"
      },
      "execution_count": null,
      "outputs": []
    }
  ]
}