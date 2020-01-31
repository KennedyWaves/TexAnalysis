using System;
using System.IO;
using System.Collections.Generic;


namespace Preprocessor
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("C# PRE-PROCESSOR FOR WHATSAPP! WORKS BETTER THAN PYTHON!");
            string linesText = File.ReadAllText("_chat.txt");
            linesText = linesText.Replace("\r\n[", "§@§");
            linesText = linesText.Replace("\r\n", " ");
            string[] lines = linesText.Replace("§@§", "\r\n[").Split("\r\n");
            for (int x = 0; x < lines.Length; x++)
            {
                int textStarts = lines[x].IndexOf(": ");
                if (lines[x] == "" || (lines[x].IndexOf("[") == 0 && lines[x].IndexOf("]") == 20 && textStarts == -1))
                {
                    lines[x] = "";
                    continue;
                }
                bool stop = false;
                string[] filterCond = new string[] { "foi removido", " imagem ocultada", "foi adicionado(a)", "Essa mensagem foi apagada.", "vídeo omitido", "áudio ocultado" };
                foreach (string value in filterCond)
                {
                    if (lines[x].IndexOf(value) > -1)
                    {
                        stop = true;
                        lines[x] = "";
                        break;
                    }
                }
                if (stop)
                {
                    continue;
                }
                if (lines[x].IndexOf("[") == 0 && lines[x].IndexOf("]") == 20 && textStarts > -1)
                {
                    using (StreamWriter sw = File.AppendText("preprocessado.txt"))
                    {
                        sw.WriteLine(lines[x]);
                        Console.WriteLine(lines[x]);
                    }
                    
                }

            }
        }
    }
}
