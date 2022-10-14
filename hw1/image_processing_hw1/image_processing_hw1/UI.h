#pragma once

namespace imageprocessinghw1 {

	using namespace System;
	using namespace System::ComponentModel;
	using namespace System::Collections;
	using namespace System::Windows::Forms;
	using namespace System::Data;
	using namespace System::Drawing;
	/// <summary>
	/// UI ���K�n
	/// </summary>

	public ref class UI : public System::Windows::Forms::Form
	{
	public:
		UI(void)
		{
			InitializeComponent();
			//
			//TODO:  �b���[�J�غc�禡�{���X
			//
			
		}
	private: System::Windows::Forms::Label^ Thresholding_label;
	private: System::Windows::Forms::Label^ Edge_Overlapping_label;
	public:

	public:

	private: System::Windows::Forms::Label^ label1;
	private: System::Windows::Forms::Label^ label2;
	private: System::Windows::Forms::Label^ label3;
	private: System::Windows::Forms::Label^ label4;
		Bitmap^ last_step_img;
		void bubble_sort(int input[], int length)
		{
			int tmp;
			for (int i = 0; i < length - 1; i++) 
			{
				for (int j = 0; j < length - i - 1; j++) 
				{
					if (input[j] > input[j + 1]) {
						tmp = input[j];
						input[j] = input[j + 1];
						input[j + 1] = tmp;
					}
				}
			}
		}
		void vertical_sobel(Bitmap^ origin, Bitmap^ processed)
		{
			int filter[3][3] = { {1,2,1},{0,0,0},{-1,-2,-1} };
			int row, col;
			Color c;
			for (int i = 0; i < origin->Width; i++)
			{
				for (int j = 0; j < origin->Height; j++)
				{
					int sum = 0;
					for (int i_offset = -1; i_offset <= 1; i_offset++)
					{
						for (int j_offset = -1; j_offset <= 1; j_offset++)
						{
							row = i + i_offset;
							col = j + j_offset;
							if (row < 0 || row >= origin->Width || col < 0 || col >= origin->Height)
								continue;
							c = origin->GetPixel(row, col);
							sum += c.R * filter[i_offset + 1][j_offset + 1];
						}
					}
					if (sum < 0) sum = -sum;
					if (sum > 255) sum = 255;
					processed->SetPixel(i, j, Color::FromArgb(sum, sum, sum));
				}
			}
		}
		void horizontal_sobel(Bitmap^ origin, Bitmap^ processed)
		{
			int filter[3][3] = { {1,0,-1},{2,0,-2},{1,0,-1} };
			int row, col;
			Color c;
			for (int i = 0; i < origin->Width; i++)
			{
				for (int j = 0; j < origin->Height; j++)
				{
					int sum = 0;
					for (int i_offset = -1; i_offset <= 1; i_offset++)
					{
						for (int j_offset = -1; j_offset <= 1; j_offset++)
						{
							row = i + i_offset;
							col = j + j_offset;
							if (row < 0 || row >= origin->Width || col < 0 || col >= origin->Height)
								continue;
							c = origin->GetPixel(row, col);
							sum += c.R * filter[i_offset + 1][j_offset + 1];
						}
					}
					if (sum < 0) sum = -sum;
					if (sum > 255) sum = 255;
					processed->SetPixel(i, j, Color::FromArgb(sum, sum, sum));
				}
			}
		}
	protected:
		/// <summary>
		/// �M������ϥΤ����귽�C
		/// </summary>
		~UI()
		{
			if (components)
			{
				delete components;
			}
		}
	private: System::Windows::Forms::Button^ R_btn;
	protected:
	private: System::Windows::Forms::GroupBox^ groupBox1;
	private: System::Windows::Forms::Button^ G_btn;
	private: System::Windows::Forms::Button^ B_btn;
	private: System::Windows::Forms::Button^ Grayscale_btn;



	private: System::Windows::Forms::GroupBox^ groupBox2;
	private: System::Windows::Forms::Button^ Median_Filter_btn;

	private: System::Windows::Forms::Button^ Mean_Filter_btn;


	private: System::Windows::Forms::GroupBox^ groupBox3;
	private: System::Windows::Forms::Button^ Histogram_btn;
	private: System::Windows::Forms::GroupBox^ groupBox4;
	private: System::Windows::Forms::TrackBar^ Threshold_bar;
	private: System::Windows::Forms::Button^ Thresholding_start_btn;
	private: System::Windows::Forms::GroupBox^ groupBox5;
	private: System::Windows::Forms::Button^ Horizontal_btn;
	private: System::Windows::Forms::Button^ Vertical_btn;
	private: System::Windows::Forms::Button^ Combined_btn;
	private: System::Windows::Forms::GroupBox^ Edge_Overlapping;
	private: System::Windows::Forms::TrackBar^ Edge_Overlapping_bar;
	private: System::Windows::Forms::Button^ Edge_Overlapping_btn;
	private: System::Windows::Forms::GroupBox^ groupBox6;
	private: System::Windows::Forms::Button^ Image_Registration_btn;
	private: System::Windows::Forms::GroupBox^ groupBox7;
	private: System::Windows::Forms::Button^ Undo_btn;
	private: System::Windows::Forms::Button^ Save_btn;
	private: System::Windows::Forms::Button^ Load_btn;
	private: System::Windows::Forms::PictureBox^ img_box1;
	private: System::Windows::Forms::PictureBox^ img_box2;
	private: System::Windows::Forms::DataVisualization::Charting::Chart^ chart1;
	private: System::Windows::Forms::DataVisualization::Charting::Chart^ chart2;
	private: System::Windows::Forms::OpenFileDialog^ openFileDialog1;
	private: System::Windows::Forms::SaveFileDialog^ saveFileDialog1;




	protected:

	private:
		/// <summary>
		/// �]�p�u��һݪ��ܼơC
		/// </summary>
		System::ComponentModel::Container ^components;

#pragma region Windows Form Designer generated code
		/// <summary>
		/// �����]�p�u��䴩�һݪ���k - �ФŨϥε{���X�s�边�ק�
		/// �o�Ӥ�k�����e�C
		/// </summary>
		void InitializeComponent(void)
		{
			System::Windows::Forms::DataVisualization::Charting::ChartArea^ chartArea1 = (gcnew System::Windows::Forms::DataVisualization::Charting::ChartArea());
			System::Windows::Forms::DataVisualization::Charting::Legend^ legend1 = (gcnew System::Windows::Forms::DataVisualization::Charting::Legend());
			System::Windows::Forms::DataVisualization::Charting::Series^ series1 = (gcnew System::Windows::Forms::DataVisualization::Charting::Series());
			System::Windows::Forms::DataVisualization::Charting::ChartArea^ chartArea2 = (gcnew System::Windows::Forms::DataVisualization::Charting::ChartArea());
			System::Windows::Forms::DataVisualization::Charting::Legend^ legend2 = (gcnew System::Windows::Forms::DataVisualization::Charting::Legend());
			System::Windows::Forms::DataVisualization::Charting::Series^ series2 = (gcnew System::Windows::Forms::DataVisualization::Charting::Series());
			this->R_btn = (gcnew System::Windows::Forms::Button());
			this->groupBox1 = (gcnew System::Windows::Forms::GroupBox());
			this->G_btn = (gcnew System::Windows::Forms::Button());
			this->B_btn = (gcnew System::Windows::Forms::Button());
			this->Grayscale_btn = (gcnew System::Windows::Forms::Button());
			this->groupBox2 = (gcnew System::Windows::Forms::GroupBox());
			this->Median_Filter_btn = (gcnew System::Windows::Forms::Button());
			this->Mean_Filter_btn = (gcnew System::Windows::Forms::Button());
			this->groupBox3 = (gcnew System::Windows::Forms::GroupBox());
			this->Histogram_btn = (gcnew System::Windows::Forms::Button());
			this->groupBox4 = (gcnew System::Windows::Forms::GroupBox());
			this->Thresholding_label = (gcnew System::Windows::Forms::Label());
			this->Threshold_bar = (gcnew System::Windows::Forms::TrackBar());
			this->Thresholding_start_btn = (gcnew System::Windows::Forms::Button());
			this->groupBox5 = (gcnew System::Windows::Forms::GroupBox());
			this->Combined_btn = (gcnew System::Windows::Forms::Button());
			this->Horizontal_btn = (gcnew System::Windows::Forms::Button());
			this->Vertical_btn = (gcnew System::Windows::Forms::Button());
			this->Edge_Overlapping = (gcnew System::Windows::Forms::GroupBox());
			this->Edge_Overlapping_label = (gcnew System::Windows::Forms::Label());
			this->Edge_Overlapping_bar = (gcnew System::Windows::Forms::TrackBar());
			this->Edge_Overlapping_btn = (gcnew System::Windows::Forms::Button());
			this->groupBox6 = (gcnew System::Windows::Forms::GroupBox());
			this->Image_Registration_btn = (gcnew System::Windows::Forms::Button());
			this->groupBox7 = (gcnew System::Windows::Forms::GroupBox());
			this->Undo_btn = (gcnew System::Windows::Forms::Button());
			this->Save_btn = (gcnew System::Windows::Forms::Button());
			this->Load_btn = (gcnew System::Windows::Forms::Button());
			this->img_box1 = (gcnew System::Windows::Forms::PictureBox());
			this->img_box2 = (gcnew System::Windows::Forms::PictureBox());
			this->chart1 = (gcnew System::Windows::Forms::DataVisualization::Charting::Chart());
			this->chart2 = (gcnew System::Windows::Forms::DataVisualization::Charting::Chart());
			this->openFileDialog1 = (gcnew System::Windows::Forms::OpenFileDialog());
			this->saveFileDialog1 = (gcnew System::Windows::Forms::SaveFileDialog());
			this->label1 = (gcnew System::Windows::Forms::Label());
			this->label2 = (gcnew System::Windows::Forms::Label());
			this->label3 = (gcnew System::Windows::Forms::Label());
			this->label4 = (gcnew System::Windows::Forms::Label());
			this->groupBox1->SuspendLayout();
			this->groupBox2->SuspendLayout();
			this->groupBox3->SuspendLayout();
			this->groupBox4->SuspendLayout();
			(cli::safe_cast<System::ComponentModel::ISupportInitialize^>(this->Threshold_bar))->BeginInit();
			this->groupBox5->SuspendLayout();
			this->Edge_Overlapping->SuspendLayout();
			(cli::safe_cast<System::ComponentModel::ISupportInitialize^>(this->Edge_Overlapping_bar))->BeginInit();
			this->groupBox6->SuspendLayout();
			this->groupBox7->SuspendLayout();
			(cli::safe_cast<System::ComponentModel::ISupportInitialize^>(this->img_box1))->BeginInit();
			(cli::safe_cast<System::ComponentModel::ISupportInitialize^>(this->img_box2))->BeginInit();
			(cli::safe_cast<System::ComponentModel::ISupportInitialize^>(this->chart1))->BeginInit();
			(cli::safe_cast<System::ComponentModel::ISupportInitialize^>(this->chart2))->BeginInit();
			this->SuspendLayout();
			// 
			// R_btn
			// 
			this->R_btn->Font = (gcnew System::Drawing::Font(L"�s�ө���", 10));
			this->R_btn->Location = System::Drawing::Point(24, 30);
			this->R_btn->Name = L"R_btn";
			this->R_btn->Size = System::Drawing::Size(86, 32);
			this->R_btn->TabIndex = 0;
			this->R_btn->Text = L"R";
			this->R_btn->UseVisualStyleBackColor = true;
			this->R_btn->Click += gcnew System::EventHandler(this, &UI::R_btn_Click);
			// 
			// groupBox1
			// 
			this->groupBox1->Controls->Add(this->G_btn);
			this->groupBox1->Controls->Add(this->B_btn);
			this->groupBox1->Controls->Add(this->Grayscale_btn);
			this->groupBox1->Controls->Add(this->R_btn);
			this->groupBox1->Font = (gcnew System::Drawing::Font(L"�s�ө���", 12));
			this->groupBox1->Location = System::Drawing::Point(22, 12);
			this->groupBox1->Name = L"groupBox1";
			this->groupBox1->Size = System::Drawing::Size(248, 141);
			this->groupBox1->TabIndex = 1;
			this->groupBox1->TabStop = false;
			this->groupBox1->Text = L"Extraction";
			// 
			// G_btn
			// 
			this->G_btn->Font = (gcnew System::Drawing::Font(L"�s�ө���", 10));
			this->G_btn->Location = System::Drawing::Point(125, 30);
			this->G_btn->Name = L"G_btn";
			this->G_btn->Size = System::Drawing::Size(86, 32);
			this->G_btn->TabIndex = 3;
			this->G_btn->Text = L"G";
			this->G_btn->UseVisualStyleBackColor = true;
			this->G_btn->Click += gcnew System::EventHandler(this, &UI::G_btn_Click);
			// 
			// B_btn
			// 
			this->B_btn->Font = (gcnew System::Drawing::Font(L"�s�ө���", 10));
			this->B_btn->Location = System::Drawing::Point(24, 85);
			this->B_btn->Name = L"B_btn";
			this->B_btn->Size = System::Drawing::Size(86, 32);
			this->B_btn->TabIndex = 2;
			this->B_btn->Text = L"B";
			this->B_btn->UseVisualStyleBackColor = true;
			this->B_btn->Click += gcnew System::EventHandler(this, &UI::B_btn_Click);
			// 
			// Grayscale_btn
			// 
			this->Grayscale_btn->Font = (gcnew System::Drawing::Font(L"�s�ө���", 10));
			this->Grayscale_btn->Location = System::Drawing::Point(125, 85);
			this->Grayscale_btn->Name = L"Grayscale_btn";
			this->Grayscale_btn->Size = System::Drawing::Size(104, 32);
			this->Grayscale_btn->TabIndex = 1;
			this->Grayscale_btn->Text = L"Grayscale";
			this->Grayscale_btn->UseVisualStyleBackColor = true;
			this->Grayscale_btn->Click += gcnew System::EventHandler(this, &UI::Grayscale_btn_Click);
			// 
			// groupBox2
			// 
			this->groupBox2->Controls->Add(this->Median_Filter_btn);
			this->groupBox2->Controls->Add(this->Mean_Filter_btn);
			this->groupBox2->Font = (gcnew System::Drawing::Font(L"�s�ө���", 12));
			this->groupBox2->Location = System::Drawing::Point(22, 172);
			this->groupBox2->Name = L"groupBox2";
			this->groupBox2->Size = System::Drawing::Size(248, 82);
			this->groupBox2->TabIndex = 4;
			this->groupBox2->TabStop = false;
			this->groupBox2->Text = L"Smooth Filter";
			// 
			// Median_Filter_btn
			// 
			this->Median_Filter_btn->Font = (gcnew System::Drawing::Font(L"�s�ө���", 10));
			this->Median_Filter_btn->Location = System::Drawing::Point(125, 30);
			this->Median_Filter_btn->Name = L"Median_Filter_btn";
			this->Median_Filter_btn->Size = System::Drawing::Size(117, 32);
			this->Median_Filter_btn->TabIndex = 3;
			this->Median_Filter_btn->Text = L"Median Filter";
			this->Median_Filter_btn->UseVisualStyleBackColor = true;
			this->Median_Filter_btn->Click += gcnew System::EventHandler(this, &UI::Median_Filter_btn_Click);
			// 
			// Mean_Filter_btn
			// 
			this->Mean_Filter_btn->Font = (gcnew System::Drawing::Font(L"�s�ө���", 10));
			this->Mean_Filter_btn->Location = System::Drawing::Point(16, 30);
			this->Mean_Filter_btn->Name = L"Mean_Filter_btn";
			this->Mean_Filter_btn->Size = System::Drawing::Size(95, 32);
			this->Mean_Filter_btn->TabIndex = 0;
			this->Mean_Filter_btn->Text = L"Mean Filter";
			this->Mean_Filter_btn->UseVisualStyleBackColor = true;
			this->Mean_Filter_btn->Click += gcnew System::EventHandler(this, &UI::Mean_Filter_btn_Click);
			// 
			// groupBox3
			// 
			this->groupBox3->Controls->Add(this->Histogram_btn);
			this->groupBox3->Font = (gcnew System::Drawing::Font(L"�s�ө���", 12));
			this->groupBox3->Location = System::Drawing::Point(22, 275);
			this->groupBox3->Name = L"groupBox3";
			this->groupBox3->Size = System::Drawing::Size(248, 82);
			this->groupBox3->TabIndex = 5;
			this->groupBox3->TabStop = false;
			this->groupBox3->Text = L"Equalization";
			// 
			// Histogram_btn
			// 
			this->Histogram_btn->Font = (gcnew System::Drawing::Font(L"�s�ө���", 10));
			this->Histogram_btn->Location = System::Drawing::Point(31, 30);
			this->Histogram_btn->Name = L"Histogram_btn";
			this->Histogram_btn->Size = System::Drawing::Size(181, 32);
			this->Histogram_btn->TabIndex = 3;
			this->Histogram_btn->Text = L"Histogram Equalization";
			this->Histogram_btn->UseVisualStyleBackColor = true;
			this->Histogram_btn->Click += gcnew System::EventHandler(this, &UI::Histogram_btn_Click);
			// 
			// groupBox4
			// 
			this->groupBox4->Controls->Add(this->Thresholding_label);
			this->groupBox4->Controls->Add(this->Threshold_bar);
			this->groupBox4->Controls->Add(this->Thresholding_start_btn);
			this->groupBox4->Font = (gcnew System::Drawing::Font(L"�s�ө���", 12));
			this->groupBox4->Location = System::Drawing::Point(22, 384);
			this->groupBox4->Name = L"groupBox4";
			this->groupBox4->Size = System::Drawing::Size(248, 98);
			this->groupBox4->TabIndex = 6;
			this->groupBox4->TabStop = false;
			this->groupBox4->Text = L"Thresholding";
			// 
			// Thresholding_label
			// 
			this->Thresholding_label->AutoSize = true;
			this->Thresholding_label->Location = System::Drawing::Point(68, 66);
			this->Thresholding_label->Name = L"Thresholding_label";
			this->Thresholding_label->Size = System::Drawing::Size(18, 20);
			this->Thresholding_label->TabIndex = 8;
			this->Thresholding_label->Text = L"0";
			// 
			// Threshold_bar
			// 
			this->Threshold_bar->Location = System::Drawing::Point(16, 30);
			this->Threshold_bar->Maximum = 255;
			this->Threshold_bar->Name = L"Threshold_bar";
			this->Threshold_bar->Size = System::Drawing::Size(130, 56);
			this->Threshold_bar->TabIndex = 7;
			this->Threshold_bar->Scroll += gcnew System::EventHandler(this, &UI::Threshold_bar_Scroll);
			// 
			// Thresholding_start_btn
			// 
			this->Thresholding_start_btn->Font = (gcnew System::Drawing::Font(L"�s�ө���", 10));
			this->Thresholding_start_btn->Location = System::Drawing::Point(164, 30);
			this->Thresholding_start_btn->Name = L"Thresholding_start_btn";
			this->Thresholding_start_btn->Size = System::Drawing::Size(65, 32);
			this->Thresholding_start_btn->TabIndex = 3;
			this->Thresholding_start_btn->Text = L"Start";
			this->Thresholding_start_btn->UseVisualStyleBackColor = true;
			this->Thresholding_start_btn->Click += gcnew System::EventHandler(this, &UI::Thresholding_start_btn_Click);
			// 
			// groupBox5
			// 
			this->groupBox5->Controls->Add(this->Combined_btn);
			this->groupBox5->Controls->Add(this->Horizontal_btn);
			this->groupBox5->Controls->Add(this->Vertical_btn);
			this->groupBox5->Font = (gcnew System::Drawing::Font(L"�s�ө���", 12));
			this->groupBox5->Location = System::Drawing::Point(22, 488);
			this->groupBox5->Name = L"groupBox5";
			this->groupBox5->Size = System::Drawing::Size(277, 82);
			this->groupBox5->TabIndex = 5;
			this->groupBox5->TabStop = false;
			this->groupBox5->Text = L"Sobel Edge Detection";
			// 
			// Combined_btn
			// 
			this->Combined_btn->Font = (gcnew System::Drawing::Font(L"�s�ө���", 10));
			this->Combined_btn->Location = System::Drawing::Point(185, 30);
			this->Combined_btn->Name = L"Combined_btn";
			this->Combined_btn->Size = System::Drawing::Size(86, 32);
			this->Combined_btn->TabIndex = 4;
			this->Combined_btn->Text = L"Combined";
			this->Combined_btn->UseVisualStyleBackColor = true;
			this->Combined_btn->Click += gcnew System::EventHandler(this, &UI::Combined_btn_Click);
			// 
			// Horizontal_btn
			// 
			this->Horizontal_btn->Font = (gcnew System::Drawing::Font(L"�s�ө���", 10));
			this->Horizontal_btn->Location = System::Drawing::Point(92, 30);
			this->Horizontal_btn->Name = L"Horizontal_btn";
			this->Horizontal_btn->Size = System::Drawing::Size(87, 32);
			this->Horizontal_btn->TabIndex = 3;
			this->Horizontal_btn->Text = L"Horizontal";
			this->Horizontal_btn->UseVisualStyleBackColor = true;
			this->Horizontal_btn->Click += gcnew System::EventHandler(this, &UI::Horizontal_btn_Click);
			// 
			// Vertical_btn
			// 
			this->Vertical_btn->Font = (gcnew System::Drawing::Font(L"�s�ө���", 10));
			this->Vertical_btn->Location = System::Drawing::Point(6, 30);
			this->Vertical_btn->Name = L"Vertical_btn";
			this->Vertical_btn->Size = System::Drawing::Size(80, 32);
			this->Vertical_btn->TabIndex = 0;
			this->Vertical_btn->Text = L"Vertical";
			this->Vertical_btn->UseVisualStyleBackColor = true;
			this->Vertical_btn->Click += gcnew System::EventHandler(this, &UI::Vertical_btn_Click);
			// 
			// Edge_Overlapping
			// 
			this->Edge_Overlapping->Controls->Add(this->Edge_Overlapping_label);
			this->Edge_Overlapping->Controls->Add(this->Edge_Overlapping_bar);
			this->Edge_Overlapping->Controls->Add(this->Edge_Overlapping_btn);
			this->Edge_Overlapping->Font = (gcnew System::Drawing::Font(L"�s�ө���", 12));
			this->Edge_Overlapping->Location = System::Drawing::Point(22, 586);
			this->Edge_Overlapping->Name = L"Edge_Overlapping";
			this->Edge_Overlapping->Size = System::Drawing::Size(286, 98);
			this->Edge_Overlapping->TabIndex = 8;
			this->Edge_Overlapping->TabStop = false;
			this->Edge_Overlapping->Text = L"Edge Overlapping";
			// 
			// Edge_Overlapping_label
			// 
			this->Edge_Overlapping_label->AutoSize = true;
			this->Edge_Overlapping_label->Location = System::Drawing::Point(56, 77);
			this->Edge_Overlapping_label->Name = L"Edge_Overlapping_label";
			this->Edge_Overlapping_label->Size = System::Drawing::Size(18, 20);
			this->Edge_Overlapping_label->TabIndex = 8;
			this->Edge_Overlapping_label->Text = L"0";
			// 
			// Edge_Overlapping_bar
			// 
			this->Edge_Overlapping_bar->Location = System::Drawing::Point(16, 30);
			this->Edge_Overlapping_bar->Name = L"Edge_Overlapping_bar";
			this->Edge_Overlapping_bar->Size = System::Drawing::Size(124, 56);
			this->Edge_Overlapping_bar->TabIndex = 7;
			this->Edge_Overlapping_bar->Scroll += gcnew System::EventHandler(this, &UI::Edge_Overlapping_bar_Scroll);
			// 
			// Edge_Overlapping_btn
			// 
			this->Edge_Overlapping_btn->Font = (gcnew System::Drawing::Font(L"�s�ө���", 10));
			this->Edge_Overlapping_btn->Location = System::Drawing::Point(143, 30);
			this->Edge_Overlapping_btn->Name = L"Edge_Overlapping_btn";
			this->Edge_Overlapping_btn->Size = System::Drawing::Size(134, 32);
			this->Edge_Overlapping_btn->TabIndex = 3;
			this->Edge_Overlapping_btn->Text = L"Edge Overlapping";
			this->Edge_Overlapping_btn->UseVisualStyleBackColor = true;
			this->Edge_Overlapping_btn->Click += gcnew System::EventHandler(this, &UI::Edge_Overlapping_btn_Click);
			// 
			// groupBox6
			// 
			this->groupBox6->Controls->Add(this->Image_Registration_btn);
			this->groupBox6->Font = (gcnew System::Drawing::Font(L"�s�ө���", 12));
			this->groupBox6->Location = System::Drawing::Point(22, 704);
			this->groupBox6->Name = L"groupBox6";
			this->groupBox6->Size = System::Drawing::Size(248, 82);
			this->groupBox6->TabIndex = 6;
			this->groupBox6->TabStop = false;
			this->groupBox6->Text = L"Image Registration";
			// 
			// Image_Registration_btn
			// 
			this->Image_Registration_btn->Font = (gcnew System::Drawing::Font(L"�s�ө���", 10));
			this->Image_Registration_btn->Location = System::Drawing::Point(31, 30);
			this->Image_Registration_btn->Name = L"Image_Registration_btn";
			this->Image_Registration_btn->Size = System::Drawing::Size(181, 32);
			this->Image_Registration_btn->TabIndex = 3;
			this->Image_Registration_btn->Text = L"Image Registration";
			this->Image_Registration_btn->UseVisualStyleBackColor = true;
			this->Image_Registration_btn->Click += gcnew System::EventHandler(this, &UI::Image_Registration_btn_Click);
			// 
			// groupBox7
			// 
			this->groupBox7->Controls->Add(this->Undo_btn);
			this->groupBox7->Controls->Add(this->Save_btn);
			this->groupBox7->Controls->Add(this->Load_btn);
			this->groupBox7->Font = (gcnew System::Drawing::Font(L"�s�ө���", 12));
			this->groupBox7->Location = System::Drawing::Point(22, 803);
			this->groupBox7->Name = L"groupBox7";
			this->groupBox7->Size = System::Drawing::Size(277, 82);
			this->groupBox7->TabIndex = 6;
			this->groupBox7->TabStop = false;
			this->groupBox7->Text = L"Function";
			// 
			// Undo_btn
			// 
			this->Undo_btn->Font = (gcnew System::Drawing::Font(L"�s�ө���", 10));
			this->Undo_btn->Location = System::Drawing::Point(185, 30);
			this->Undo_btn->Name = L"Undo_btn";
			this->Undo_btn->Size = System::Drawing::Size(80, 32);
			this->Undo_btn->TabIndex = 4;
			this->Undo_btn->Text = L"Undo";
			this->Undo_btn->UseVisualStyleBackColor = true;
			this->Undo_btn->Click += gcnew System::EventHandler(this, &UI::Undo_btn_Click);
			// 
			// Save_btn
			// 
			this->Save_btn->Font = (gcnew System::Drawing::Font(L"�s�ө���", 10));
			this->Save_btn->Location = System::Drawing::Point(92, 30);
			this->Save_btn->Name = L"Save_btn";
			this->Save_btn->Size = System::Drawing::Size(87, 32);
			this->Save_btn->TabIndex = 3;
			this->Save_btn->Text = L"Save";
			this->Save_btn->UseVisualStyleBackColor = true;
			this->Save_btn->Click += gcnew System::EventHandler(this, &UI::Save_btn_Click);
			// 
			// Load_btn
			// 
			this->Load_btn->Font = (gcnew System::Drawing::Font(L"�s�ө���", 10));
			this->Load_btn->Location = System::Drawing::Point(6, 30);
			this->Load_btn->Name = L"Load_btn";
			this->Load_btn->Size = System::Drawing::Size(80, 32);
			this->Load_btn->TabIndex = 0;
			this->Load_btn->Text = L"Load";
			this->Load_btn->UseVisualStyleBackColor = true;
			this->Load_btn->Click += gcnew System::EventHandler(this, &UI::Load_btn_Click);
			// 
			// img_box1
			// 
			this->img_box1->Location = System::Drawing::Point(326, 27);
			this->img_box1->Name = L"img_box1";
			this->img_box1->Size = System::Drawing::Size(512, 384);
			this->img_box1->TabIndex = 9;
			this->img_box1->TabStop = false;
			// 
			// img_box2
			// 
			this->img_box2->Location = System::Drawing::Point(326, 463);
			this->img_box2->Name = L"img_box2";
			this->img_box2->Size = System::Drawing::Size(512, 384);
			this->img_box2->TabIndex = 10;
			this->img_box2->TabStop = false;
			// 
			// chart1
			// 
			chartArea1->Name = L"ChartArea1";
			this->chart1->ChartAreas->Add(chartArea1);
			legend1->Name = L"Legend1";
			this->chart1->Legends->Add(legend1);
			this->chart1->Location = System::Drawing::Point(903, 27);
			this->chart1->Name = L"chart1";
			series1->ChartArea = L"ChartArea1";
			series1->Legend = L"Legend1";
			series1->Name = L"Series1";
			this->chart1->Series->Add(series1);
			this->chart1->Size = System::Drawing::Size(493, 384);
			this->chart1->TabIndex = 11;
			this->chart1->Text = L"chart1";
			// 
			// chart2
			// 
			chartArea2->Name = L"ChartArea1";
			this->chart2->ChartAreas->Add(chartArea2);
			legend2->Name = L"Legend1";
			this->chart2->Legends->Add(legend2);
			this->chart2->Location = System::Drawing::Point(903, 463);
			this->chart2->Name = L"chart2";
			series2->ChartArea = L"ChartArea1";
			series2->Legend = L"Legend1";
			series2->Name = L"Series1";
			this->chart2->Series->Add(series2);
			this->chart2->Size = System::Drawing::Size(493, 384);
			this->chart2->TabIndex = 12;
			this->chart2->Text = L"chart2";
			// 
			// openFileDialog1
			// 
			this->openFileDialog1->FileName = L"openFileDialog1";
			// 
			// label1
			// 
			this->label1->AutoSize = true;
			this->label1->Font = (gcnew System::Drawing::Font(L"�s�ө���", 12));
			this->label1->Location = System::Drawing::Point(1125, 4);
			this->label1->Name = L"label1";
			this->label1->Size = System::Drawing::Size(59, 20);
			this->label1->TabIndex = 13;
			this->label1->Text = L"Before";
			// 
			// label2
			// 
			this->label2->AutoSize = true;
			this->label2->Font = (gcnew System::Drawing::Font(L"�s�ө���", 12));
			this->label2->Location = System::Drawing::Point(1125, 426);
			this->label2->Name = L"label2";
			this->label2->Size = System::Drawing::Size(48, 20);
			this->label2->TabIndex = 14;
			this->label2->Text = L"After";
			// 
			// label3
			// 
			this->label3->AutoSize = true;
			this->label3->Font = (gcnew System::Drawing::Font(L"�s�ө���", 12));
			this->label3->Location = System::Drawing::Point(537, 4);
			this->label3->Name = L"label3";
			this->label3->Size = System::Drawing::Size(57, 20);
			this->label3->TabIndex = 15;
			this->label3->Text = L"Origin";
			// 
			// label4
			// 
			this->label4->AutoSize = true;
			this->label4->Font = (gcnew System::Drawing::Font(L"�s�ө���", 12));
			this->label4->Location = System::Drawing::Point(537, 426);
			this->label4->Name = L"label4";
			this->label4->Size = System::Drawing::Size(81, 20);
			this->label4->TabIndex = 16;
			this->label4->Text = L"Processed";
			// 
			// UI
			// 
			this->AutoScaleDimensions = System::Drawing::SizeF(8, 15);
			this->AutoScaleMode = System::Windows::Forms::AutoScaleMode::Font;
			this->ClientSize = System::Drawing::Size(1438, 943);
			this->Controls->Add(this->label4);
			this->Controls->Add(this->label3);
			this->Controls->Add(this->label2);
			this->Controls->Add(this->label1);
			this->Controls->Add(this->chart2);
			this->Controls->Add(this->chart1);
			this->Controls->Add(this->img_box2);
			this->Controls->Add(this->img_box1);
			this->Controls->Add(this->groupBox7);
			this->Controls->Add(this->groupBox6);
			this->Controls->Add(this->Edge_Overlapping);
			this->Controls->Add(this->groupBox5);
			this->Controls->Add(this->groupBox4);
			this->Controls->Add(this->groupBox3);
			this->Controls->Add(this->groupBox2);
			this->Controls->Add(this->groupBox1);
			this->Name = L"UI";
			this->Text = L"UI";
			this->groupBox1->ResumeLayout(false);
			this->groupBox2->ResumeLayout(false);
			this->groupBox3->ResumeLayout(false);
			this->groupBox4->ResumeLayout(false);
			this->groupBox4->PerformLayout();
			(cli::safe_cast<System::ComponentModel::ISupportInitialize^>(this->Threshold_bar))->EndInit();
			this->groupBox5->ResumeLayout(false);
			this->Edge_Overlapping->ResumeLayout(false);
			this->Edge_Overlapping->PerformLayout();
			(cli::safe_cast<System::ComponentModel::ISupportInitialize^>(this->Edge_Overlapping_bar))->EndInit();
			this->groupBox6->ResumeLayout(false);
			this->groupBox7->ResumeLayout(false);
			(cli::safe_cast<System::ComponentModel::ISupportInitialize^>(this->img_box1))->EndInit();
			(cli::safe_cast<System::ComponentModel::ISupportInitialize^>(this->img_box2))->EndInit();
			(cli::safe_cast<System::ComponentModel::ISupportInitialize^>(this->chart1))->EndInit();
			(cli::safe_cast<System::ComponentModel::ISupportInitialize^>(this->chart2))->EndInit();
			this->ResumeLayout(false);
			this->PerformLayout();

		}
#pragma endregion
private: System::Void Load_btn_Click(System::Object^ sender, System::EventArgs^ e)
{
	if(openFileDialog1->ShowDialog() == System::Windows::Forms::DialogResult::OK)
	{
		Bitmap^ openImg = gcnew Bitmap(openFileDialog1->FileName);
		//Bitmap^ temp = gcnew Bitmap(openImg->Width, openImg->Height);
		img_box1->Image = openImg;
		//for (int i = 0; i < temp->Height; i++)
		//	for (int j = 0; j < temp->Width; j++)
		//	{
		//		Color RGB = openImg->GetPixel(j, i);
	
		//		int invR = Convert::ToInt32(255 - RGB.R);
		//		int invG = Convert::ToInt32(255 - RGB.G);
		//		int invB = Convert::ToInt32(255 - RGB.B);
	
		//		temp->SetPixel(j, i, Color::FromArgb(invR, invG, invB));
		//	}
		img_box2->Image = openImg;
		last_step_img = openImg;
	}
}

private: System::Void Save_btn_Click(System::Object^ sender, System::EventArgs^ e)
{
	if (!(img_box2->Image)) return;
	
	saveFileDialog1->Filter = "JPeg Image|*.jpg|Bitmap Image|*.bmp|Gif Image|*.gif";
	saveFileDialog1->Title = "Save an Image File";

	if (saveFileDialog1->ShowDialog() == System::Windows::Forms::DialogResult::OK) {
		String^ sfd = saveFileDialog1->FileName;

		img_box2->Image->Save(sfd, System::Drawing::Imaging::ImageFormat::Jpeg);
	}
}
private: System::Void Undo_btn_Click(System::Object^ sender, System::EventArgs^ e)
{
	img_box2->Image = last_step_img;
}

/*****************  Extraction *****************/
private: System::Void R_btn_Click(System::Object^ sender, System::EventArgs^ e)
{
	if (!(img_box2->Image)) return;
	last_step_img = gcnew Bitmap(img_box2->Image);
	Bitmap^ copy = gcnew Bitmap(img_box2->Image);
	
	for (int i = 0; i < copy->Width; i++)
		for (int j = 0; j < copy->Height; j++)
		{
			Color c = copy->GetPixel(i, j);
			int r = c.R;
			copy->SetPixel(i, j, Color::FromArgb(r, r, r));
		}
	img_box2->Image = copy;
}
private: System::Void G_btn_Click(System::Object^ sender, System::EventArgs^ e)
{
	if (!(img_box2->Image)) return;
	last_step_img = gcnew Bitmap(img_box2->Image);
	Bitmap^ copy = gcnew Bitmap(img_box2->Image);

	for (int i = 0; i < copy->Width; i++)
		for (int j = 0; j < copy->Height; j++)
		{
			Color c = copy->GetPixel(i, j);
			int r = c.G;
			copy->SetPixel(i, j, Color::FromArgb(r, r, r));
		}
	img_box2->Image = copy;
}
private: System::Void B_btn_Click(System::Object^ sender, System::EventArgs^ e)
{
	if (!(img_box2->Image)) return;
	last_step_img = gcnew Bitmap(img_box2->Image);
	Bitmap^ copy = gcnew Bitmap(img_box2->Image);

	for (int i = 0; i < copy->Width; i++)
		for (int j = 0; j < copy->Height; j++)
		{
			Color c = copy->GetPixel(i, j);
			int r = c.B;
			copy->SetPixel(i, j, Color::FromArgb(r, r, r));
		}
	img_box2->Image = copy;
}
private: System::Void Grayscale_btn_Click(System::Object^ sender, System::EventArgs^ e)
{
	if (!(img_box2->Image)) return;
	last_step_img = gcnew Bitmap(img_box2->Image);
	Bitmap^ copy = gcnew Bitmap(img_box2->Image);

	for (int i = 0; i < copy->Width; i++)
	{
		for (int j = 0; j < copy->Height; j++)
		{
			Color c = copy->GetPixel(i, j);
			int r = c.R * 0.299 + c.G * 0.587 + c.B * 0.114;
			copy->SetPixel(i, j, Color::FromArgb(r, r, r));
		}
	}
		
	img_box2->Image = copy;
}

/*****************  Extraction *****************/

private: System::Void Mean_Filter_btn_Click(System::Object^ sender, System::EventArgs^ e)
{
	if (!(img_box2->Image)) return;
	Bitmap^ origin = gcnew Bitmap(img_box2->Image);
	last_step_img = origin;
	Bitmap^ processed = gcnew Bitmap(img_box2->Image);
	int row, col;
	Color c;
	for (int i = 0; i < origin->Width; i++)
	{
		for (int j = 0; j < origin->Height; j++)
		{
			int mean = 0;
			for (int i_offset = -1; i_offset <= 1; i_offset++)
			{
				for (int j_offset = -1; j_offset <= 1; j_offset++)
				{
					row = i + i_offset;
					col = j + j_offset;
					if (row < 0 || row >= origin->Width || col < 0 || col >= origin->Height)
						continue;
					c = origin->GetPixel(row, col);
					mean += c.R;
				}
			}
			mean /= 9;
			processed->SetPixel(i, j, Color::FromArgb(mean, mean, mean));
		}
	}

	img_box2->Image = processed;
}
private: System::Void Median_Filter_btn_Click(System::Object^ sender, System::EventArgs^ e)
{
	if (!(img_box2->Image)) return;
	Bitmap^ origin = gcnew Bitmap(img_box2->Image);
	last_step_img = origin;
	Bitmap^ processed = gcnew Bitmap(img_box2->Image);
	int row, col;
	Color c;
	int list[9];// = new int(9);
	for (int i = 0; i < origin->Width; i++)
	{
		for (int j = 0; j < origin->Height; j++)
		{
			int count = 0;
			for (int i_offset = -1; i_offset <= 1; i_offset++)
			{
				for (int j_offset = -1; j_offset <= 1; j_offset++)
				{
					row = i + i_offset;
					col = j + j_offset;
					if (row < 0 || row >= origin->Width || col < 0 || col >= origin->Height)
					{
						list[count++] = 0;
					}
					else
					{
						c = origin->GetPixel(row, col);
						list[count++] = c.R;
					}
				}
			}
			count++;
			bubble_sort(list, 9);
			processed->SetPixel(i, j, Color::FromArgb(list[4], list[4], list[4]));
		}
	}
	img_box2->Image = processed;
}
/*****************  Extraction *****************/
private: System::Void Histogram_btn_Click(System::Object^ sender, System::EventArgs^ e)
{
	if (!(img_box2->Image)) return;
	chart1->Series["Series1"]->Points->Clear();
	chart2->Series["Series1"]->Points->Clear();
	last_step_img = gcnew Bitmap(img_box2->Image);
	Bitmap^ copy = gcnew Bitmap(img_box2->Image);
	Color c;
	int gray[256];
	int processed_gray[256];
	float accumulation[256];
	int mapping[256];
	for (int i = 0; i <= 255; i++)
	{
		gray[i] = 0;
		processed_gray[i] = 0;
	}
	for (int i = 0; i < copy->Width; i++)
	{
		for (int j = 0; j < copy->Height; j++)
		{
			c = copy->GetPixel(i, j);
			gray[c.R]++;
		}
	}

	int area = copy->Width * copy->Height;
	accumulation[0] = gray[0] / area;
	for (int i = 1; i <= 255; i++) accumulation[i] = accumulation[i - 1] + ((float)(gray[i]) / area);
	for (int i = 0; i <= 255; i++)
	{
		mapping[i] = (int)Math::Floor(accumulation[i] * 255);
		processed_gray[mapping[i]] += gray[i];
	}
	// Set Chart
	for (int i = 0; i <= 255; i++)
	{
		chart1->Series["Series1"]->Points->AddXY(i, gray[i]);
		chart2->Series["Series1"]->Points->AddXY(i, processed_gray[i]);
	}
	// Process image
	int value = 0;
	for (int i = 0; i < copy->Width; i++)
	{
		for (int j = 0; j < copy->Height; j++)
		{
			c = copy->GetPixel(i, j);
			value = mapping[c.R];
			copy->SetPixel(i, j, Color::FromArgb(value, value, value));
		}
	}
	img_box2->Image = copy;
}

/*****************  Extraction *****************/
//private: System::Void Threshold_bar_Scroll(System::Object^ sender, System::EventArgs^ e)
//{
//}
private: System::Void Thresholding_start_btn_Click(System::Object^ sender, System::EventArgs^ e)
{
	if (!(img_box2->Image)) return;
	last_step_img = gcnew Bitmap(img_box2->Image);
	Bitmap^ copy = gcnew Bitmap(img_box2->Image);
	Color c;
	int threshold = Threshold_bar->Value;
	int value;
	for (int i = 0; i < copy->Width; i++)
	{
		for (int j = 0; j < copy->Height; j++)
		{
			c = copy->GetPixel(i, j);
			value = c.R;
			if (value >= threshold) value = 255;
			copy->SetPixel(i, j, Color::FromArgb(value, value, value));
		}
	}
	img_box2->Image = copy;
}
	   /*****************  Extraction *****************/
private: System::Void Vertical_btn_Click(System::Object^ sender, System::EventArgs^ e)
{
	if (!(img_box2->Image)) return;
	Bitmap^ origin = gcnew Bitmap(img_box2->Image);
	Bitmap^ processed = gcnew Bitmap(img_box2->Image);
	last_step_img = origin;
	vertical_sobel(origin, processed);
	img_box2->Image = processed;
}
private: System::Void Horizontal_btn_Click(System::Object^ sender, System::EventArgs^ e)
{
	if (!(img_box2->Image)) return;
	Bitmap^ origin = gcnew Bitmap(img_box2->Image);
	last_step_img = origin;
	Bitmap^ processed = gcnew Bitmap(img_box2->Image);

	horizontal_sobel(origin, processed);
	img_box2->Image = processed;
}
private: System::Void Combined_btn_Click(System::Object^ sender, System::EventArgs^ e)
{
	last_step_img = gcnew Bitmap(img_box2->Image);
	Bitmap^ copy = gcnew Bitmap(img_box2->Image);
	Bitmap^ vertical = gcnew Bitmap(img_box2->Image);
	Bitmap^ horizontal = gcnew Bitmap(img_box2->Image);
	vertical_sobel(copy, vertical);
	vertical_sobel(copy, horizontal);
	Color c1, c2;
	for (int i = 0; i < copy->Width; i++)
	{
		for (int j = 0; j < copy->Height; j++)
		{
			c1 = vertical->GetPixel(i, j);
			c2 = horizontal->GetPixel(i, j);
			int sobel = (int)(Math::Sqrt(c1.R * c1.R + c2.R * c2.R));
			if (sobel > 255)
				sobel = 255;
			copy->SetPixel(i, j, Color::FromArgb(sobel, sobel, sobel));
		}
	}
	img_box2->Image = copy;
}


private: System::Void Edge_Overlapping_bar_Scroll(System::Object^ sender, System::EventArgs^ e)
{
}
private: System::Void Edge_Overlapping_btn_Click(System::Object^ sender, System::EventArgs^ e)
{
}

private: System::Void Image_Registration_btn_Click(System::Object^ sender, System::EventArgs^ e)
{
}
private: System::Void Threshold_bar_Scroll(System::Object^ sender, System::EventArgs^ e) 
{
	int value = Threshold_bar->Value;
	Thresholding_label->Text = Convert::ToString(value);
}
};
}
